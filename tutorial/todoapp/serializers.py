from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.todoapp.models import TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['title', 'description','user_created',]


class TodoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)

    def create(self, validated_data):
        todoItem = TodoItem.objects.create(**validated_data)
        username = self.context["username"]
        todoItem.user = User.objects.get(username=username)
        todoItem.save()
        return todoItem

    def update(self, instance, validated_data):
        # instance.email = validated_data.get('email', instance.email)
        # instance.content = validated_data.get('content', instance.content)
        # instance.created = validated_data.get('created', instance.created)
        return instance


class TodoOutputSerializer(serializers.ModelSerializer):
    user_created = serializers.SerializerMethodField('get_user_created')

    def get_user_created(self, todo):
        if todo.user:
            return todo.user.username
        return ""

    class Meta:
        model = TodoItem
        fields = ['title', 'description','user_created',]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( 'email', 'username', 'password','first_name', 'last_name')
        required_spec_dict = {
            'required': True,
            'allow_blank': False
        }
        extra_kwargs = {
            'email': required_spec_dict,
            'first_name': required_spec_dict,
            'last_name': required_spec_dict
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
