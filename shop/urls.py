from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='ShopHome'),
    path("about/", views.about, name='AboutUs'),
    path("tracker/", views.Tracker, name='tracking_status'),
    path("contact/", views.Contact, name='ContactUs'),
    path("searchResult/", views.search, name='searchResult'),
    path("productView/<int:prod_id>", views.productView, name='productView'),
    path("checkout/", views.checkout, name='checkout'),
    path("cart/", views.cart, name='cart')
]