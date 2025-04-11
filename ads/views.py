from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Item, Ad, ExchangeOffer
from .forms import AdForm

def item_list(request):
    ads = Item.objects.all()
    return JsonResponse({'ads': list(ads.values())})

def item_detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        return JsonResponse({'item': {'id': item.id, 'name': item.name, 'description': item.description}})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

def ad_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')
    
    ads = Ad.objects.all()
    
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)
    
    return render(request, 'ads/ad_list.html', {'ads': ads})

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
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Объявление успешно создано!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании объявления. Проверьте введенные данные.")
        return super().form_invalid(form)

class AdUpdateView(UpdateView):
    model = Ad
    template_name = 'ads/ad_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('ad-list')

class AdDeleteView(DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Объявление успешно удалено!")
        return super().delete(request, *args, **kwargs)

def create_proposal(request, pk):
    # Логика для создания предложения
    return JsonResponse({'message': 'Proposal created successfully'})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ads:ad-detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def update_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором этого объявления.")
    
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad-detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором этого объявления.")
    
    if request.method == 'POST':
        ad.delete()
        return redirect('ads:ad-list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def create_exchange_offer(request):
    if request.method == 'POST':
        ad_sender_id = request.POST.get('ad_sender_id')
        ad_receiver_id = request.POST.get('ad_receiver_id')
        comment = request.POST.get('comment')

        ad_sender = get_object_or_404(Ad, id=ad_sender_id, user=request.user)
        ad_receiver = get_object_or_404(Ad, id=ad_receiver_id)

        offer = ExchangeOffer.objects.create(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment=comment
        )
        return redirect('ads:ad-list')

    return render(request, 'ads/exchange_offer_form.html')

@login_required
def update_exchange_offer(request, pk):
    offer = get_object_or_404(ExchangeOffer, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(ExchangeOffer.STATUS_CHOICES):
            offer.status = status
            offer.save()
            return redirect('ads:ad-list')
    return render(request, 'ads/exchange_offer_update.html', {'offer': offer})

@login_required
def exchange_offer_list(request):
    offers = ExchangeOffer.objects.all()

    sender_id = request.GET.get('sender_id')
    receiver_id = request.GET.get('receiver_id')
    status = request.GET.get('status')

    if sender_id:
        offers = offers.filter(ad_sender_id=sender_id)
    if receiver_id:
        offers = offers.filter(ad_receiver_id=receiver_id)
    if status:
        offers = offers.filter(status=status)

    return render(request, 'ads/exchange_offer_list.html', {'offers': offers})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'ads/register.html', {'form': form})