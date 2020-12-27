from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tutorial.todoapp.models import TodoItem
from tutorial.todoapp.serializers import TodoItemSerializer


class TodoItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed and edited
    """
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated]
