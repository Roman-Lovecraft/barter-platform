from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.ad_list, name='ad-list'),
    path('<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('new/', views.create_ad, name='ad-create'),
    path('<int:pk>/update/', views.update_ad, name='ad-update'),
    path('<int:pk>/delete/', views.delete_ad, name='ad-delete'),
    path('register/', views.register, name='register'),
    path('exchange-offers/', views.exchange_offer_list, name='exchange-offer-list'),
    path('exchange-offers/new/', views.create_exchange_offer, name='exchange-offer-create'),
    path('exchange-offers/<int:pk>/update/', views.update_exchange_offer, name='exchange-offer-update'),
]