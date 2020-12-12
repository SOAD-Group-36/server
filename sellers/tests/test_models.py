from utils.address import Address
from django.test import TestCase
from sellers.models import Seller
import datetime as dt


class SellerModelTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
            'first_name': "Bob", 'last_name': "builder", "phone": '1234567890', 'address': Address('123456', 'ss', 'cc', 'll', 'hn', 'sn'),
            'pan': 'VKVG2URU2R', 'gst': '556876t97', 'webhook_url': 'http://localhost:8080/webhook/'
        }
        self.seller = Seller.objects.create(**self.data)
    
    def test_model_creation(self):
        self.assertTrue(Seller.objects.filter(first_name=self.data['first_name']).exists())

    def test_name(self):
        self.assertEqual(self.seller.first_name, self.data['first_name'])
        self.assertEqual(self.seller.last_name, self.data['last_name'])

    def test_phone(self):
        self.assertEqual(self.seller.phone, self.data['phone'])

    def test_address(self):
        self.assertEqual(self.seller.address, self.data['address'])

    def test_pan(self):
        self.assertEqual(self.seller.pan, self.data['pan'])

    def test_gst(self):
        self.assertEqual(self.seller.gst, self.data['gst'])

    def test_webhook_url(self):
        self.assertEqual(self.seller.webhook_url, self.data['webhook_url'])
