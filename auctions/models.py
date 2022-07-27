from pickle import TRUE
from statistics import mode
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass

class Category(models.Model):
    OTHER = 'OTHER'
    CLOTHING = 'CLOTHING'
    MAGICAL_ITEM = 'MAGICAL_ITEM'
    TOYS_KIDS = 'TOYS_KIDS'
    HEALTH_BEAUTY = 'HEALTH_BEAUTY'
    FOOD = 'FOOD'
    WEAPONS = 'WEAPONS'
    HOUSEHOLDS = 'HOUSEHOLD_ITEMS'
    

    CATEGORIES = [
        (OTHER, 'OTHER'),
        (CLOTHING, 'CLOTHING'),
        (MAGICAL_ITEM, 'MAGICAL ITEMS'),
        (TOYS_KIDS, 'TOYS & KIDS'),
        (HEALTH_BEAUTY, 'HEALTH & BEAUTY'),
        (FOOD, 'FOOD'),
        (WEAPONS, 'WEAPONS'),
        (HOUSEHOLDS, 'HOUSEHOLD ITEMS')
        
    ]

    categories = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default=OTHER,
    )

    def __str__(self):
        return self.categories


class AuctionListing(models.Model):
    
    title=models.CharField(max_length=64)
    description = models.CharField(blank = True, max_length=1000)
    picture = models.URLField()
    time_posted = models.DateField(auto_now_add = True)
    num_of_bids = models.IntegerField(default=0) 
    starting_bid = models.FloatField()    
    current_price = models.FloatField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", max_length=50, null=True )
    # title - des - pict - time - start - owner - current - numof

    def __str__(self):
        return f"{self.id}: {self.title} | {self.starting_bid} | {self.current_price} | {self.owner}"


# represent a bid placed by an user
class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "bids_listing")
    value = models.FloatField()

    def __str__(self):
        return f"{self.value} on {self.listing} by {self.bidder}"


class Comments(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content=models.TextField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment_listing")
    time_posted = models.DateField(auto_now=True)

    def __str__(self):
        return f"comments made on {self.listing} by {self.author}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "listing")

    def __str__(self):
        return f"{self.id}: {self.user} added {self.listing}"

