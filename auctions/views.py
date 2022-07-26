
from distutils.log import error
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":

        #get data
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting-bid"]
        image = request.POST["image"]

        #create object
        listing = AuctionListing(title=title, description=description, picture=image, starting_bid=starting_bid, owner=get_user(request) )
        listing.save()

    return render(request, "auctions/create-listing.html")

def listing(request, title, id):
    listing = AuctionListing.objects.get(pk=id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "title": title,
        })

#normal check is_owner function
def is_owner(request, listing):
    current_user = get_user(request)
    owner = listing.owner

    if current_user == owner:
        return True
    else:
        return False

def listing_auth(request, title, id):
    listing = AuctionListing.objects.get(pk=id)

   
    if Watchlist.objects.filter(user=get_user(request), listing= listing).exists():
        added = True
    else:
        added = False
    
    winner = None
    is_current_user = False
    #find the winner
    if not listing.active:
        if listing.num_of_bids > 0:
            winner = Bids.objects.get(listing=listing, value=listing.current_price).bidder
            if winner == get_user(request):
                is_current_user = True

    return render(request, "auctions/listing_authenticated.html", {
        "listing": listing,
        "title": title,
        "added": added,
        "is_owner": is_owner(request, listing),
        "winner": winner,
        "is_current_user_winner": is_current_user
        })
   
def watchlistAdd(request, id):

    #listing = AuctionListing.objects.get(pk=id)
    listing = get_object_or_404(AuctionListing, pk=id)

    saved_listing = Watchlist(user=get_user(request), listing=listing)
    saved_listing.save()
        
    return HttpResponseRedirect(reverse("listing_auth", kwargs={"title": listing.title, "id": id}))

def remove_from_watchlist(request, id):

    listing = get_object_or_404(AuctionListing, pk=id)
    user = get_user(request)

    instance = Watchlist.objects.filter(user=user, listing=listing)
    instance.delete()

    return HttpResponseRedirect(reverse("listing_auth", kwargs={"title": listing.title, "id": id}))   
    
@login_required
def watchlist(request):
    user = get_user(request)

    lists = Watchlist.objects.filter(user=user).values_list('listing', flat=True)

    listings = []
    for l in lists:
        listings.append(AuctionListing.objects.get(pk=l))

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def place_bid(request, id):
    listing = AuctionListing.objects.get(pk=id)

    if request.method == "POST":
        bid_value = float(request.POST["bid_value"])
        if bid_value >= listing.starting_bid and bid_value > listing.current_price:
            #create bid
            bid = Bids(bidder=get_user(request), listing=listing, value=bid_value)
            bid.save()
            #update listing data
            AuctionListing.objects.filter(id=id).update(current_price = bid_value, num_of_bids = listing.num_of_bids + 1)
            #pop up message
            messages.add_message(request, messages.SUCCESS, f"Bids of value {bid_value} successfully placed.")
        else:
            messages.add_message(request, messages.ERROR, "Bids must be of value larger than current price!")
    
    return HttpResponseRedirect(reverse("listing_auth", kwargs={"title": listing.title, "id": id}))

@login_required
def close_bid(request, id):
    try:
        listing = AuctionListing.objects.get(pk=id)
        listing.active = False
        listing.save()
    except:
        error("Models do not exist")

    return HttpResponseRedirect(reverse("listing_auth", kwargs={"title": listing.title, "id": id}))

def category(request):
    pass
