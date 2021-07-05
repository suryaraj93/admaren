from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import exceptions, serializers

from textSaver.models import Tag, Text


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        # obj = User.objects.get(username=username)
        # print(obj.username)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            data['user'] = user
        else:
            msg = 'login failed'
            raise exceptions.ValidationError(msg)
        return data


class TagSerializer(serializers.ModelSerializer):

    # texts = TextSerializer(source='text_set')
    class Meta:
        model = Tag
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    created_user = serializers.StringRelatedField()

    class Meta:
        model = Text
        fields = "text_title", "tag", "timestamp", "created_user"
        depth = 1


class OverViewSerializer(serializers.HyperlinkedModelSerializer):
    snippet_count = serializers.SerializerMethodField()

    class Meta:
        model = Text
        fields = ["text_title", "snippet_count"]
        depth = 2

    def get_snippet_count(self, obj):

        snippet_count = Text.objects.filter(text_title=obj).count()
        return snippet_count
