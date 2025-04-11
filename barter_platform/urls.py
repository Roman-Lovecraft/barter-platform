from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ads import views as ads_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]