import hashlib

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import parsers, renderers
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User
from .utils import *
from .serializers import (
	UserSerializer,
	UserLoginSerializer
)

# users/
class ListUsers(APIView):

	def get(self, request, format=None):
	    if request.method == 'GET':
	        users = User.objects.all()
	        serializer = UserSerializer(users, many=True)
	        return Response(serializer.data)

	def post(self, request, format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			print("SERIALIZER")
			print(serializer)
			print("SERIALIZER.DATA")
			print(serializer.data)
			print("SERIALIZER.ERRORS")
			print(serializer.errors)
			return Response(serializer.data, status=HTTP_200_OK)
		return Resp0nse(serializer.errors, status=400)

# user/[id]
class ListUser(APIView):
	def get(self, request, pk, format=None):
		try:
			user = User.objects.get(pk=pk)
		except User.DoesNotExist:
			return HttpResponse(status=404)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		try:
			user = User.objects.get(pk=pk)
		except User.DoesNotExist:
		    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
		serializer = UserSerializer(data=request.data,partial=True)
		if serializer.is_valid():
			new_user = request.data
			token = request.META['HTTP_AUTHORIZATION']
			if not token:
				return Response("The user token is required", status=400)
			first_name = ""
			last_name = ""
			email = ""
			password = ""
			if 'first_name' in new_user:
				first_name = new_user['first_name']
			else:
				first_name = user.first_name
			if 'last_name' in new_user:
				last_name = new_user['last_name']
			else:
				last_name = user.last_name
			displayname = first_name + " " + last_name
			if 'email' in new_user:
				email = new_user['email']
			else:
				email = user.email
			if 'password' in new_user:
				password = new_user['password']
				password_is_valid = validatePassword(password)
				if password_is_valid != True:
					raise ValidationError(password_is_valid)
					return
				password = crypt_password(new_user['password'])
			else:
				password = user.password

			user_id =  user.user_id
			created_at = user.created_at
			user_to_save = User(token=token,first_name=first_name,last_name=last_name,displayname=displayname,password=password,email=email,user_id=user_id,created_at=created_at)
			user_to_save.save()
			return Response(UserSerializer(user_to_save).data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		try:
			user = User.objects.get(pk=pk)
		except User.DoesNotExist:
		    return HttpResponse(status=404)
		user.delete()
		return Response(True,status=HTTP_200_OK)

#Login
class ListLogin(APIView):
	
	def post(self, request, *args, **kwargs):
		serializer = UserLoginSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
































