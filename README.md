# DRF Todo List Back-End
This project is intended to learn about the Django REST framework and build a todo list Back-end.
Current the todo list back-end supports Creating, Updating, Deleting , Viewing Todo Lists.


### Supported Endpoints

- Creating User : localhost/users/
- Creating and Viewing TodoList(requires basic auth): localhost/todonew/
- View Todo Detail (requires basic auth): localhost/todonew/todoid/

### Todo item security
A todo item can be created only with authenticated requests. An user can view only his todo lists and update and delete them.
