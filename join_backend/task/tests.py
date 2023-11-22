from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

class LoginViewTest(TestCase):
    def setUp(self):
   
        self.user = CustomUser.objects.create_user(
            user_name='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_login_view(self):
     
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = client.post('/log_in/', data, format='json')
        print(response.status_code)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)

    def test_invalid_login_view(self):

        client = APIClient()
        invalid_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }
        response = client.post('/log_in/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


 


