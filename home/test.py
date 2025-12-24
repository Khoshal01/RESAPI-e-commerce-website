from rest_framework.test import APITestCase 
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import ProductModel , OrderModel

class TestSetup(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="amin",
            password="T2332330"
        )

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.product_url = reverse('myproduct-list')
        self.order_url = reverse('myorders-list')

class RegisterViewTest(TestSetup):

    def test_register(self):
        data = {
            "username": "ali",
            "email": "ali@gmail.com",
            "password": "Test12345",
            "password2": "Test12345",
            "role": "customer"
        }
        res = self.client.post(self.register_url, data, format='json')
        self.assertEqual(res.status_code, 201)



class LoginTest(TestSetup):

    def test_login(self):
        data = {
            "username": "amin",
            "password": "T2332330"
        }
        res = self.client.post(self.login_url, data, format='json')
        self.assertEqual(res.status_code, 200)


    def test_login(self):

        data = {
            "username": "amin",
            "password": "T2332330"
        }
        res = self.client.post(self.login_url, data, format='json')
        self.assertEqual(res.status_code, 200)


class ProductTestCase(TestSetup):

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)

        self.product = ProductModel.objects.create(
            owner=self.user,
            product_name='desktop',
            description='wow',
            quantity=12,
            price=1000
        )

    def test_get_product(self):
        res = self.client.get(self.product_url)
        self.assertEqual(res.status_code, 200)

    def test_post_product(self):
        data = {
            "product_name": "laptop",
            "description": "good",
            " stock":12,
            "price": 2000
        }
        res = self.client.post(self.product_url, data, format='json')
        self.assertEqual(res.status_code, 201)



class OrderTest(TestSetup):

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)

        self.order = OrderModel.objects.create(
            orderowner=self.user,
            order_items="laptop",
            total_price=12000
        )

    def test_post_order(self):
        data = {
            "order_items": "mouse",
            "total_price": 500
        }
        res = self.client.post(self.order_url, data, format='json')
        self.assertEqual(res.status_code, 201)


    

        
    

 