from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from tutorial.todoapp.models import TodoItem
from tutorial.todoapp.serializers import TodoItemSerializer, TodoOutputSerializer, TodoInputSerializer, UserSerializer, \
    TodoUpdateSerializer


class TodoItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed and edited
    """
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated]


class TodoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    only for list and post
    '''
    def get(self, request, format=None):
        todos = TodoItem.objects.filter(user__username=request.user.username)
        serializer = TodoOutputSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoInputSerializer(data=request.data.copy())
        serializer.context["username"] = request.user.username #passing username, serializer will add the linked user later
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailAPIView(APIView):
    """
    Retrieve, update or delete a todoitem instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return TodoItem.objects.get(pk=pk)
        except TodoItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoOutputSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        todo = self.get_object(pk)
        request_username = request.user.username
        todo_username = ""
        if todo.user:
            todo_username = todo.user.username
        if request_username!=todo_username:
            raise ValidationError("You are not allowed to perform this action.")

        serializer = TodoUpdateSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        request_username = request.user.username
        todo_username = ""
        if todo.user:
            todo_username = todo.user.username
        if request_username!=todo_username:
            raise ValidationError("You are not allowed to perform this action.")
        todo.delete()
        return Response({"delete": "delete success"},status=status.HTTP_204_NO_CONTENT)



class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
