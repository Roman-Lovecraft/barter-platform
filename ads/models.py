from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TradeOffer(models.Model):
    item_offered = models.ForeignKey(Item, related_name='offers', on_delete=models.CASCADE)
    item_requested = models.ForeignKey(Item, related_name='requests', on_delete=models.CASCADE)
    proposer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.proposer.username} offers {self.item_offered.name} for {self.item_requested.name}"

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads_ads')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    category = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    ad_sender = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proposal from {self.ad_sender} to {self.ad_receiver}"

class ExchangeOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_offers')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_offers')
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer from {self.ad_sender} to {self.ad_receiver} ({self.status})"