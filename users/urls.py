from django.urls import path
from .views import AdCreateView, AdUpdateView, AdDeleteView, AdDetailView

urlpatterns = [
    path('new/', AdCreateView.as_view(), name='ad-create'),
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='ad-edit'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
]