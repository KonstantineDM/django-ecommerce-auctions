from django.urls import path


from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("listing/<int:listing_id>", views.view_listing, name="listing"),
    path("<int:user_id>/create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.close_listing, name="close_listing"),

    path("listing/<int:listing_id>/bid", views.bid_add, name="bid"),

    path("<int:user_id>/watchlist", views.watchlist_view, name="watchlist"),
    path("listing/<int:listing_id>/watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("listing/<int:listing_id>/watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
    
    path("listing/<int:listing_id>/comment_add", views.comment_add, name="comment_add"),
    path("listing/<int:listing_id>/comment_view", views.comment_view, name="comment_view"),

    path("categories", views.categories, name="categories"),
    path("category/<int:cat_id>", views.category_listings, name="category_listings"),
]
