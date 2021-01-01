from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import RequestsClient, APIClient
from django.urls import reverse


# Create your tests here.
from ..todoapp.models import TodoItem


class TodoItemModelTests(TestCase):

    def test_check_default_values(self):
        """
        create a todo item with just the required values and see if the other items value are prefilled
        with default values
        """
        todoitem = TodoItem(title='test title',description='test description')
        self.assertIs(todoitem.is_completed, False)
        self.assertIs(todoitem.priority, 5)

    def test_foreignkey_value(self):
        """
        create a todo item with just the required values and see if the other items value are prefilled
        with default values
        """
        todoitem = TodoItem(title='test title',description='test description')
        testuser = User(username='testuser',email='test@test.com')
        testuser.set_password("12345678")
        todoitem.user = testuser
        self.assertIsNotNone(todoitem.user)


class UserCreationAPITests(TestCase):
    def test_create_user_without_required_params(self):
        request_body = {
            'username': 'testusername',
            'email': 'a@a.com'
        }
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_success_case(self):
        request_body = {
            'username': 'testusername',
            'email': 'a@a.com',
            'password':'12345678',
            'first_name':'test first name',
            'last_name': 'test last name'
        }
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_same_username(self):
        request_body = {
            'username': 'testusername',
            'email': 'a@a.com',
            'password':'12345678',
            'first_name':'test first name',
            'last_name': 'test last name'
        }
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def get_todo_request_body():
    return {
            'title': 'todotitle',
            'description': 'testdesc',
            'due_datetime':'20-01-2020 15:20'
        }


class TodoCreationAPITests(TestCase):

    def test_create_todo_unauthenticated(self):
        body_params = get_todo_request_body()
        client = APIClient()
        response = client.post('/todonew/', body_params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
