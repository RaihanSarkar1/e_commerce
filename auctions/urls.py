from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("auction_listing/<str:auction_listing_id>", views.auction_listing, name="auction_listing"),
    path("add/<str:auction_listing_id>", views.add_watchlist, name="add_watchlist"),
    path("rem/<str:auction_listing_id>", views.rem_watchlist, name="rem_watchlist"),
    path("bid/<str:auction_listing_id>", views.bid, name="bid"),
    path("close/<str:auction_listing_id>", views.close, name="close"),
    path("comment/<str:auction_listing_id>", views.comment, name="comment"),
    path("category/<str:category>", views.category_item, name="category_item")



    



]
