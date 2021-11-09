from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Category, Comment, Listing, User, Bid, Watchlist
from .forms import ListingForm
from .utils import get_max_bid, is_watched


def index(request):
    context = {
        "listings": Listing.objects.all()
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request, user_id):
    # Create new listing as a logged-in User
    user = User.objects.get(pk=user_id)
    date = timezone.now()

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            
            listing = form.save(commit=False)
            listing.user = user
            form.save()
            
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            context = {"form": form}
            return render(request, "auctions/create_listing.html", context)
    else:
        form = ListingForm()

    context = {
        "form": form,
        "user": user, 
        "date": date,
    }
    return render(request, "auctions/create_listing.html", context)


def view_listing(request, listing_id):
    # View existing listing via its page
    listing = Listing.objects.get(pk=listing_id)
    watched = is_watched(request, listing_id)

    context = {"listing": listing, "watched": watched}
    return render(request, "auctions/view_listing.html", context)

@login_required
def close_listing(request, listing_id):
    # If auction is done, mark the listing as closed (inactive), declare the winner 
    listing = Listing.objects.get(pk=listing_id)
    bid_list = Bid.objects.all().filter(listing=listing.id)
    winner = bid_list.last().user.username

    listing.active = False
    listing.winner = winner
    listing.save()

    context = {"listing": listing}
    return render(request, "auctions/view_listing.html", context)

@login_required
def bid_add(request, listing_id):
    # Add a bid to listing (checks for it to be greater than current max bid)
    listing = Listing.objects.get(pk=listing_id)
    max_bid = get_max_bid(listing_id)
    if request.method == "POST":
        bid_price = int(request.POST["bid"])
        context = {"listing": listing, "message_error": "Your bid must be higher that the current price."}

        if not max_bid:
            if bid_price >= int(listing.price):
                bid = Bid(user=request.user, size=bid_price, listing=listing)
                bid.save()
                listing.bid = bid
                listing.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
            else:
                return render(request, "auctions/view_listing.html", context)

        elif max_bid:
            if bid_price > max(int(listing.price), int(max_bid)):
                bid = Bid(user=request.user, size=bid_price, listing_id=listing.id)
                bid.save()
                listing.bid = bid
                listing.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
            else:
                return render(request, "auctions/view_listing.html", context)
    
    else:
        context = {"listing": listing}
        return render(request, "auctions/view_listing.html", context)

@login_required
def watchlist_add(request, listing_id):
    # Add currently viewed listing to logged-in User's watchlist
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist(user=request.user, listing=listing)
    watchlist.save()

    watchlist_list = Watchlist.objects.all().filter(user=request.user)

    context = {"watchlist": watchlist_list, "listing": listing,}
    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

@login_required
def watchlist_remove(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.all().filter(user=request.user, listing=listing)
    watchlist.delete()

    watchlist = Watchlist.objects.all().filter(user=request.user, listing=listing)
    
    return HttpResponseRedirect(reverse("auctions:watchlist", args=(request.user.id,)))

@login_required
def watchlist_view(request, user_id):
    watchlist = Watchlist.objects.all().filter(user=request.user)

    context = {"watchlist": watchlist}
    return render(request, "auctions/watchlist.html", context)

@login_required
def comment_add(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watched = is_watched(request, listing_id)
    if request.method == "POST":
        text = request.POST["text"]
        author  = User.objects.get(pk=request.user.id)
        comment = Comment(text=text, author=author, listing=listing)
        comment.save()
        context = {"listing": listing}
        return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
    else:
        context = {"listing": listing, "watched": watched}
    
    return render(request, "auctions/view_listing.html", context)


def comment_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.all().filter(listing=listing)

    context = {"comments": comments}
    return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))


def categories(request):
    # Show list of existing categories of listings
    categories = Category.objects.all()

    context = {"categories": categories}
    return render(request, "auctions/categories.html", context)


def category_listings(request, cat_id):
    # Show all listings in the chosen category
    category = Category.objects.get(pk=cat_id)
    cat_listings = Listing.objects.all().filter(category=category)

    context = {"listings": cat_listings, "category": category}
    return render(request, "auctions/category_listings.html", context)