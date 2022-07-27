from .models import *
from django.contrib import admin

# username: auctions_superuser
#email: auctions_superuser@auctions.com
#pass: auctions_superuser1234

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)