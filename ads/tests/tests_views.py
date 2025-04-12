from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeOffer

class AdTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test Description',
            category='electronics',
            condition='new'
        )

    def test_ad_list_view(self):
        response = self.client.get(reverse('ads:ad-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')

    def test_ad_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('ads:ad-create'), {
            'title': 'New Ad',
            'description': 'New Description',
            'category': 'electronics',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Ad.objects.filter(title='New Ad').exists())

    def test_ad_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('ads:ad-update', args=[self.ad.pk]), {
            'title': 'Updated Ad',
            'description': 'Updated Description',
            'category': 'electronics',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Ad')

    def test_ad_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('ads:ad-delete', args=[self.ad.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

class ExchangeOfferTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.ad1 = Ad.objects.create(user=self.user1, title='Ad 1', description='Description 1', category='electronics', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ad 2', description='Description 2', category='electronics', condition='used')

    def test_create_exchange_offer(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('ads:exchange-offer-create'), {
            'ad_sender_id': self.ad1.pk,
            'ad_receiver_id': self.ad2.pk,
            'comment': 'Test Comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeOffer.objects.filter(ad_sender=self.ad1, ad_receiver=self.ad2).exists())

    def test_update_exchange_offer(self):
        offer = ExchangeOffer.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Test Comment', status='pending')
        self.client.login(username='user2', password='password')
        response = self.client.post(reverse('ads:exchange-offer-update', args=[offer.pk]), {
            'status': 'accepted'
        })
        self.assertEqual(response.status_code, 302)
        offer.refresh_from_db()
        self.assertEqual(offer.status, 'accepted')