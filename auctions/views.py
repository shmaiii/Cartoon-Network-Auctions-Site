from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import AuctionListing, User


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
        listing = AuctionListing(title=title, description=description, picture=image, starting_bid=starting_bid, current_price=starting_bid, owner=get_user(request) )
        listing.save()

    return render(request, "auctions/create-listing.html")

def listing(request, title, id):
    return render(request, "auctions/listing.html", {
        "listing": AuctionListing.objects.get(pk=id),
        "title": title
    })

def watchlist(request):
    pass

def category(request):
    pass
