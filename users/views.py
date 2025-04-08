from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ad, ExchangeProposal
from ads.forms import AdForm, ProposalForm
from django.contrib.auth.decorators import login_required

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)
            
        return queryset.order_by('-created_at')

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad-list')
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user

@login_required
def create_proposal(request, pk):
    ad_receiver = get_object_or_404(Ad, pk=pk)
    
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = Ad.objects.filter(user=request.user).first()
            proposal.ad_receiver = ad_receiver
            proposal.save()
            return redirect('ad-detail', pk=ad_receiver.pk)
    else:
        form = ProposalForm()
    
    return render(request, 'ads/proposal_form.html', {
        'form': form,
        'ad_receiver': ad_receiver
    })