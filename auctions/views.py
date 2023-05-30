from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Auction_Listing, Bids, Comments
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class NewBidForm(forms.Form):
    bid = forms.IntegerField(label="Place a bid ")

@login_required(login_url='login')
def index(request):
    Auction_Listings = Auction_Listing.objects.all()
    return render(request, "auctions/index.html", {
        "Auction_Listings": Auction_Listings
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
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = request.POST["start_bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        creator = request.user
        auction_listing = Auction_Listing(title=title,description=description,start_bid=start_bid,image=image,category=category, creator=creator)
        auction_listing.save()
        #If create post is sucsessfull
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html")

def auction_listing(request, auction_listing_id):
    auction_listing = Auction_Listing.objects.get(pk=auction_listing_id)
    watching = True
    try:
        auction_listing.users_watching.get(username = request.user.username)
    except ObjectDoesNotExist:
        watching = False
    return render(request, "auctions/auction_listing.html",{
        "Auction_Listing": auction_listing,
        "Users_Watching": auction_listing.users_watching.all(),
        "Watching": watching,
        "form": NewBidForm(),
        "Bid": auction_listing.item_biddings.order_by("-bid").first(),
        "Comments": auction_listing.comments.all()
    })

def add_watchlist(request, auction_listing_id):
    listing = Auction_Listing.objects.get(pk=auction_listing_id)
    thisUser = request.user
    thisUser.watchlist.add(listing)
    return HttpResponseRedirect(reverse("auction_listing", args=(listing.id,)))

def rem_watchlist(request, auction_listing_id):
    listing = Auction_Listing.objects.get(pk=auction_listing_id)
    thisUser = request.user
    thisUser.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("auction_listing", args=(listing.id,)))

def watchlist(request):
    thelist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "Watchlist": thelist
    })


def bid(request, auction_listing_id):
    bid_item = Auction_Listing.objects.get(pk=auction_listing_id)
    user = request.user
    bid = int(request.POST["bid"])
    highest_bid_item = bid_item.item_biddings.order_by('-bid').first()
    if highest_bid_item != None:
        highest_bid = highest_bid_item.bid
    else:
        highest_bid = 0
    if bid > bid_item.start_bid and bid > highest_bid:
        new_bid = Bids(bid_item=bid_item, user=user, bid=bid)
        new_bid.save()
        messages.success(request, 'Placed bid successfully.')
        return HttpResponseRedirect(reverse("auction_listing", args=(bid_item.id,)))
    else:
        messages.warning(request, 'You bid amount is not higher than the highest bid or starting bid!')
        return HttpResponseRedirect(reverse("auction_listing", args=(bid_item.id,)))

def close(request, auction_listing_id):
    auction_listing = Auction_Listing.objects.get(pk=auction_listing_id)
    auction_listing.status = "closed"
    auction_listing.save()
    messages.warning(request, 'Your auction has been closed')

    return HttpResponseRedirect(reverse("auction_listing", args=(auction_listing.id,)))

def comment(request, auction_listing_id):
    auction_listing = Auction_Listing.objects.get(pk=auction_listing_id)
    user = request.user
    comment = request.POST["comment"]
    newComment = Comments(list_id = auction_listing, user = user, comment = comment)
    newComment.save()

    return HttpResponseRedirect(reverse("auction_listing", args=(auction_listing.id,)))

def categories(request):
    objectsWithUniqueCategories = Auction_Listing.objects.all().values('category').distinct()
    return render(request, "auctions/categories.html", {
        "Categories": objectsWithUniqueCategories
    })

def category_item(request, category):
    objectsWithTheCategory = Auction_Listing.objects.filter(category= category)
    return render(request, "auctions/index.html", {
        "Auction_Listings": objectsWithTheCategory
    })



