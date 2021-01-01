from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.todoapp.models import TodoItem

'''
This was the serializer in the first version of todo app back-end. it works but, we have not customized anything here
It is supposed to work with viewsets. viewsets was also used in the first version of the todo app, but later we used apiviews
to customize the apis as our need
'''
class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['title', 'description','user_created',]


class TodoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    due_datetime = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M',])
    remind_me_datetime = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M',],required=False)
    priority = serializers.ChoiceField(choices=TodoItem.PRIORITIES,required=False)
    """
    A serializer can either implement create or update methods or both as per django docs. 
    """
    def create(self, validated_data):
        todoItem = TodoItem.objects.create(**validated_data)
        username = self.context["username"]
        user_fetched = User.objects.filter(username=username).first()
        if user_fetched:
            todoItem.user = user_fetched
            todoItem.save()
        return todoItem

    def validate(self, data):
        """
        Check that the remind me date is before the before due date.
        """
        # print(data['remind_me_datetime'])
        if 'remind_me_datetime' in data:
            # remind_time = datetime.strptime(data['remind_me_datetime'], '%d-%m-%Y %H:%M')
            # due_time = datetime.strptime(data['due_datetime'], '%d-%m-%Y %H:%M')
            if not (data['due_datetime'] > data['remind_me_datetime']):
                raise serializers.ValidationError({"remind_me_date": "Reminder date has to be before due date"})
        return data

'''
This serializer is used to update todos, the reason behind creating a new serializer is, while updating all the fields
are optional, while creating, only some fields are optional
'''
class TodoUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False,max_length=100)
    description = serializers.CharField(required=False,max_length=200)
    is_completed = serializers.BooleanField(required=False)
    due_datetime = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M',],required=False)
    remind_me_datetime = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M',],required=False)
    priority = serializers.ChoiceField(choices=TodoItem.PRIORITIES,required=False)
    """
    A serializer can either implement create or update methods or both, as per django rest docs. 
    """
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data.get('title', instance.title)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        if 'is_completed' in validated_data:
            instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        if 'due_datetime' in validated_data:
            instance.due_datetime = validated_data.get('due_datetime', instance.due_datetime)
        if 'remind_me_datetime' in validated_data:
            instance.remind_me_datetime = validated_data.get('remind_me_datetime', instance.remind_me_datetime)
        if 'priority' in validated_data:
            instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance

    def validate(self, data):
        """
        Check that the remind me date is before the before due date.
        """
        # print(data['remind_me_datetime'])
        if 'remind_me_datetime' in data:
            if 'due_datetime' in data:
                if not (data['due_datetime'] > data['remind_me_datetime']):
                    raise serializers.ValidationError({"remind_me_date": "Reminder date has to be before due date"})
            else:
                instance = getattr(self, 'instance', None)
                if not (instance.due_datetime > data['remind_me_datetime']):
                    raise serializers.ValidationError({"remind_me_date": "Reminder date has to be before due date"})
        return data

'''
This serializer is used to output todos in a certain format
'''
class TodoOutputSerializer(serializers.ModelSerializer):
    user_created = serializers.SerializerMethodField('get_user_created')

    def get_user_created(self, todo):
        if todo.user:
            return todo.user.username
        return ""

    class Meta:
        model = TodoItem
        fields = ['title', 'description','due_datetime','remind_me_datetime','priority','user_created',]

'''
This serializer is used for creating new users by calling the back-end. Here we used the django auth class's user directly
'''
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
