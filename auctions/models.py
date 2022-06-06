from statistics import mode
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    class Category(models.TextChoices):
        BOOKS = 'BOOKS', _('Books')
        HEALTH_BEAUTY = "H&B", _('Health & Beauty')
        TOYS_KIDS = "T&K", _('Toys, Kids, Babies & STEM')
        SPORTS = "S&O", _('Sports, Outdoors')
        CLOTHING = "CLOTHING", _('Clothing, Shoes, Jewels')

    title=models.CharField(max_length=64)
    description = models.CharField(blank = True, max_length=1000)
    picture = models.URLField()
    time_posted = models.DateField(auto_now_add = True)
    num_of_bids = models.IntegerField()
    category = models.CharField(choices = Category.choices, max_length=50)
    starting_bid = models.FloatField()      
       

# represent a bid placed by an user
class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "bids_listing")
    value = models.FloatField()


class Comments(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content=models.CharField(max_length=1000)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment_listing")
    time_posted = models.DateField(auto_now=True)


