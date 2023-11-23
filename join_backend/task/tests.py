from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Contact, Category, Task
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer, ContactSerializer, CategorySerializer, TaskSerializer

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
        
class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  

    def test_register_user(self):
        data = {'user_name': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User successfully created')

    def test_register_invalid_data(self):
        data = {'user_name': '', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_name', response.data)  
        
class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            user_name='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.logout_url = reverse('logout')  
        
    def test_logout_user(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'successfully logged out.')
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_unauthorized_logout(self):
        self.client.credentials()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertTrue(Token.objects.filter(user=self.user).exists())

class UserViewTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(user_name='user1', email='user1@example.com', password='password1')
        self.user2 = CustomUser.objects.create_user(user_name='user2', email='user2@example.com', password='password2')
        self.client = APIClient()
        self.user_view_url = reverse('users')  

    def test_get_user_list(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['user_name'], 'user1')
        self.assertEqual(response.data[1]['user_name'], 'user2')
        expected_data = UserSerializer([self.user1, self.user2], many=True).data
        self.assertEqual(response.data, expected_data)
        
class ContactViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(user_name='testuser', email='test@example.com', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.contact_view_url = reverse('contacts')  

    def test_create_contact(self):
        # Daten für die zu erstellende Kontaktanfrage
        data = {
            'email': 'newcontact@example.com',
            'user_name': 'user1',
        }
        response = self.client.post(self.contact_view_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newcontact@example.com')
        self.assertEqual(response.data['user_name'], 'user1')

    def test_create_contact_email_in_use(self):
        existing_email = 'existing@example.com'
        Contact.objects.create(email=existing_email)
        data = {'email': existing_email,  'user_name': 'user1',}
        response = self.client.post(self.contact_view_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'Email already in use')
    
    def test_get_contacts(self):
        # Erstellen von Testkontakten
        Contact.objects.create(email='contact1@example.com', created_by=self.user)
        Contact.objects.create(email='contact2@example.com', created_by=self.user)
        response = self.client.get(self.contact_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class EditContactViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(user_name='testuser', email='test@example.com', password='testpassword')
        self.contact = Contact.objects.create(email='contact@example.com', created_by=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.edit_contact_view_url = reverse('edit_contacts', args=[self.contact.id])  

    def test_edit_contact(self):
        updated_data = {'email': 'updated_contact@example.com', 'user_name': 'Updated User', 'phone': '123', 'color': '#fff', 'initials': 'AH', 'created_by': self.user.id}
        response = self.client.put(self.edit_contact_view_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  
    def test_edit_contact_email_in_use(self):
        existing_email = 'existing@example.com'
        Contact.objects.create(email=existing_email)
        data = {'email': existing_email, 'phone': 'some_value'}
        response = self.client.put(self.edit_contact_view_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'Email already in use')

    def test_edit_contact_not_found(self):
        non_existing_contact_id = 999
        data = {'email': 'updated_contact@example.com', 'user_name': 'Updated User', 'phone': '123', 'color': '#fff', 'initials': 'AH', 'created_by': self.user.id}
        response = self.client.put(reverse('edit_contacts', args=[non_existing_contact_id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Contact not found')
 
class DeleteContactViewTest(TestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(user_name='testuser', email='test@example.com', password='testpassword')
        self.contact = Contact.objects.create(email='contact@example.com', created_by=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_delete_contact(self):
        url = reverse('delete_contact', args=[self.contact.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    def test_delete_non_existing_contact(self):
        non_existing_contact_id = 999
        url = reverse('delete_contact', args=[non_existing_contact_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Not found.')
        
class CategoryViewTest(TestCase):
    def test_post_category(self):
        data = {'title': 'New Category'}
        response = self.client.post(reverse('category'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(title='New Category').exists())

    def test_post_existing_category(self):
        Category.objects.create(title='Existing Category')
        data = {'title': 'Existing Category'}
        response = self.client.post(reverse('category'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Title already exists')

    def test_get_categories(self):
        Category.objects.create(title='Category 1')
        Category.objects.create(title='Category 2')
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_category(self):
        category = Category.objects.create(title='Category to delete')
        url = reverse('delete_category', args=[category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())

    def test_delete_non_existing_category(self):
        non_existing_category_id = 999
        url = reverse('delete_category', args=[non_existing_category_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Not found.')
        
class TaskViewTest(TestCase):
    def setUp(self):
        Task.objects.create(title='Test Task 1')

    def test_create_task(self):
        url = reverse('task')
        data = {'title': 'New Task'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)  

    def test_get_tasks(self):
        url = reverse('task')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.count())

    def test_patch_task(self):
        existing_task = Task.objects.first()
        url = reverse('task')
        data = {'id': existing_task.id, 'title': 'Updated Task'}
        response = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        existing_task.refresh_from_db()
        self.assertEqual(existing_task.title, 'Updated Task')

    def test_delete_task(self):
        existing_task = Task.objects.first()
        url = reverse('delete_task', args=[existing_task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

