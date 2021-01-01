from datetime import datetime

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


def get_user_creation_body_params():
    return {
            'username': 'testusername',
            'email': 'a@a.com',
            'password':'12345678',
            'first_name':'test first name',
            'last_name': 'test last name'
        }

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
        request_body = get_user_creation_body_params()
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_same_username(self):
        request_body = ()
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

    def test_create_todo_success(self):
        body_params = get_todo_request_body()
        user_creation_params = get_user_creation_body_params()
        user = User.objects.create_user(**user_creation_params)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/todonew/', body_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_todo_with_invalid_remind_date(self):
        body_params = get_todo_request_body()
        body_params['remind_me_datetime'] = '21-01-2020 15:20'
        user_creation_params = get_user_creation_body_params()
        user = User.objects.create_user(**user_creation_params)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/todonew/', body_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_todo_with_invalid_remind_date(self):
        user_creation_params = get_user_creation_body_params()
        user = User.objects.create_user(**user_creation_params)

        object_init_values = get_todo_request_body()
        del object_init_values['due_datetime']
        date_time_str = '20-01-2020 15:20'
        due_date_object = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M')
        todo_object = TodoItem(**object_init_values)
        todo_object.due_datetime = due_date_object
        todo_object.save()
        object_id = todo_object.id

        body_params = dict()
        body_params['remind_me_datetime'] = '21-01-2020 15:20'
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/todonew/'+str(object_id) + '/', body_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_todo_with_valid_remind_date(self):
        user_creation_params = get_user_creation_body_params()
        user = User.objects.create_user(**user_creation_params)

        object_init_values = get_todo_request_body()
        del object_init_values['due_datetime']
        date_time_str = '22-01-2020 15:20'
        due_date_object = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M')
        todo_object = TodoItem(**object_init_values)
        todo_object.due_datetime = due_date_object
        todo_object.save()
        object_id = todo_object.id

        body_params = dict()
        body_params['remind_me_datetime'] = '22-01-2020 15:19'
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/todonew/'+str(object_id) + '/', body_params)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo_updated = response.data
        self.assertEqual(todo_updated['title'],'todotitle')
