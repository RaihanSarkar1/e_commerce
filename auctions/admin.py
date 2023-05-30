from django.contrib import admin
from .models import Auction_Listing, User, Bids, Comments

class UserAdmin(admin.ModelAdmin):
    #For many to many relationships makes it easier to manipulate
    filter_horizontal = ("watchlist",)
# Register your models here.
admin.site.register(Auction_Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User, UserAdmin)
