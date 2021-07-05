from django.contrib.auth import login as djangologin
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from textSaver.models import Tag, Text
from textSaver.serializers import (LoginSerializer, OverViewSerializer,
                                   TagSerializer, TextSerializer,
                                   UserCreationSerializer)


class UserView(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserCreationSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "Registeration Successful",
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Registration failed",
                "data": serializer.data
            },
            status=status.HTTP_400_BAD_REQUEST)

# class UserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     # permission_classes = (AllowAny,)
#     serializer_class = UserCreationSerializer
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        djangologin(request, user)
        token, created = Token.objects.get_or_create(user=user)
        request.session['token'] = token.key
        request.session['userid'] = user.id
        return Response(
            {
                'message': 'You have successfully Logged in.',
                'user': user.id,
                'token': token.key
            },
            status=status.HTTP_200_OK)


class TagList(APIView):

    def get(self, request, format=None):
        query = Tag.objects.all()
        serializer = TagSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Tagdetail(APIView):

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        query = self.get_object(pk)
        serializer = TagSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        query = self.get_object(pk)
        serializer = TagSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TextView(APIView):

    def get(self, request, format=None):
        query = Text.objects.all()
        serializer = TextSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Textdetail(APIView):

    def get_object(self, pk):
        try:
            return Text.objects.get(pk=pk)
        except Text.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        query = self.get_object(pk)
        serializer = TextSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        query = self.get_object(pk)
        serializer = TextSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OverView(generics.ListAPIView):
    queryset = Text.objects.all()
    serializer_class = OverViewSerializer
