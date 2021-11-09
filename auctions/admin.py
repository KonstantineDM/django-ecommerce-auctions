from django.contrib import admin
from django.contrib.auth import models

from .models import Comment, User, Category, Bid, Listing, Watchlist

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "date", "category")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "bid_size", "date")

    def bid_size(self, obj):
        return f"{obj.size}"

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "author", "text", "date")




admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist)
admin.site.register(Comment, CommentAdmin)
