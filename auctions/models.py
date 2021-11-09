from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.utils import timezone


class User(AbstractUser):
    first_name = models.CharField(max_length=64, blank=True, help_text="Optional")
    last_name = models.CharField(max_length=64, blank=True, help_text="Optional")

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    title = models.CharField(max_length=16, default="Other")

    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return f"{self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey("Listing", null=True, on_delete=models.SET_NULL, related_name="watchlist")

    def __str__(self):
        return f"{self.user}: {self.listing}"


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids")
    size = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey("Listing", null=True, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"${self.size}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default="")
    price = models.DecimalField(max_digits=16, decimal_places=2)
    bid = models.ForeignKey(Bid, null=True, blank=True, on_delete=models.SET_NULL, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(default="", help_text="Provide a URL-link to Image", max_length=500)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="listings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, null=True, blank=True)
    
    def __str__(self):
        return (f"{self.title}")


class Comment(models.Model):
    text = models.CharField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="author")
    date = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey("Listing", null=True, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text
