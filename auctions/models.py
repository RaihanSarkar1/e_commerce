from django.contrib.auth.models import AbstractUser
from django.db import models


class Auction_Listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    start_bid = models.IntegerField()
    image = models.CharField(max_length=200)
    category = models.CharField(max_length=60)
    creator = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=6, default="active")


class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction_Listing, blank=True, related_name="users_watching")

class Bids(models.Model):
    #bid_item field- the item for which a bid has been placed
    bid_item = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="item_biddings")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_biddings")
    bid = models.IntegerField()

class Comments(models.Model):
    list_id = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=200)