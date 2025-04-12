from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Item

class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        # Передаем owner при создании объекта
        Item.objects.create(name="Test Item", description="This is a test item.", owner=self.user)

    def test_item_creation(self):
        item = Item.objects.get(name="Test Item")
        self.assertEqual(item.description, "This is a test item.")

    def test_item_str(self):
        item = Item.objects.get(name="Test Item")
        self.assertEqual(str(item), "Test Item")