from django.db import models
from django.contrib.auth.models import User

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_ads')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=[('electronics', 'Электроника'), ('clothing', 'Одежда')], default='electronics')
    condition = models.CharField(max_length=50, choices=[('new', 'Новый'), ('used', 'Б/у')], default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('declined', 'Отклонена'),
    ]
    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals', on_delete=models.CASCADE)
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals', on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal from {self.ad_sender} to {self.ad_receiver} ({self.status})"
