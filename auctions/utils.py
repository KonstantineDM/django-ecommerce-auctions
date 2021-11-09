from .models import Bid, Listing, Watchlist

# Utility fucntions

def get_max_bid(listing_id):
    # Get max bid from all bids currently added to the listing
    bid_set = Bid.objects.all().filter(listing_id=listing_id)
    bid_list = [bid.size for bid in bid_set]
    max_bid = sorted(bid_list)[-1] if bid_list else 0
    return max_bid


def is_watched(request, listing_id):
    # Check if listing is in the User's watchlist
    listing = Listing.objects.get(pk=listing_id)
    # check if user is logged in
    if request.user.username:       # request.user.username is an empty string for anonymous user
        watchlist = Watchlist.objects.all().filter(user=request.user)
    else:
        watchlist = []
    
    watched_ids = [listing.id for listing in watchlist]

    if listing.id in watched_ids:
        return True
    else:
        return False