# DRF Todo List Back-End
This project is intended to learn about the Django REST framework and build a todo list Back-end.
Current the todo list back-end supports Creating, Updating, Deleting , Viewing Todo Lists.


### Supported Endpoints

- Creating a User : localhost/users/
- Creating and Viewing TodoList(requires basic auth): localhost/todonew/
- View Todo Detail, Update and Delete (requires basic auth): localhost/todonew/todoid/

### Authentication
A todo item can be created only with authenticated requests. The project uses Basic Auth. Once a user is created by the user endpoint
, only then he will be able to create, update , delete his own todos.

### Testing
This project contatins testing classes and methods. Models, views, serializers were tested. Tests can be run using
```python
python manage.py test
```
### How to make an authenticated request
Create an user by using the users api. Then if you requesting the API with postman, select basic auth and put the username and password which you used to create
the user. If you are using Mobile or Any other platform, then put in the header the username and password
