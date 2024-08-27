from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quote/<str:symbol>/', views.quote_detail, name='quote'),
    path('remove/<str:symbol>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('add/<str:symbol>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('search/', views.search, name='search'),
]
