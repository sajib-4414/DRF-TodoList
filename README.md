# DRF Todo List Back-End
This project is intended to learn about the Django REST framework and build a todo list Back-end.
Current the todo list back-end supports Creating, Updating, Deleting , Viewing Todo Lists.


### Supported Endpoints

- Creating User : localhost/users/
- Creating and Viewing TodoList(requires basic auth): localhost/todonew/
- View Todo Detail (requires basic auth): localhost/todonew/todoid/

### Authentication
A todo item can be created only with authenticated requests. The project uses Basic Auth. Once a user is created by the user endpoint
, only then he will be able to create, update , delete his own todos.

### Testing
This project contatins testing classes and methods. Models, views, serializers were tested. Tests can be run using
```python
python manage.py test
```
