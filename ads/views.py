from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Item, Ad

def item_list(request):
    ads = Item.objects.all()
    return JsonResponse({'ads': list(ads.values())})

def item_detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        return JsonResponse({'item': {'id': item.id, 'name': item.name, 'description': item.description}})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

class AdCreateView(CreateView):
    model = Ad
    template_name = 'ads/ad_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('ad-list')

class AdUpdateView(UpdateView):
    model = Ad
    template_name = 'ads/ad_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('ad-list')

class AdDeleteView(DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad-list')

def create_proposal(request, pk):
    # Логика для создания предложения
    return JsonResponse({'message': 'Proposal created successfully'})