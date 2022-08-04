from django.urls import path

from . import views

urlpatterns = [
    path("/", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cate_each/<int:id>/", views.cate_each, name="cate_each"),
    path("createListing/", views.create_listing, name="create_listing"),
    path("<str:title>/<int:id>/", views.listing, name="listing"),
    path("<str:title>/<int:id>/auth/", views.listing_auth, name="listing_auth"),
    path("<int:id>/watchlistAdd", views.watchlistAdd, name="watchlistAdd"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid"),
    path("post_comment/<int:id>", views.post_comment, name="post_comment"),
    path("category", views.category, name="category")
]
