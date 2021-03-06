import md5
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import User
from .utils import *

import requests


class UserSerializer(ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'
		write_only_fields = ('password',)
		read_only_fields = ('id',)

	def create(self, validated_data):
		"""
		Create and return a new `User` instance, given the validated data.
		"""
		user_obj = None
		email = validated_data.get("email", None)
		if not email:
			raise ValidationError("Email is required to create an account.")
		password = ""
		fb_userId = ""
		google_userId = ""
		linkedin_token = ""
		linkedin_real_token = ""

		if 'password' in validated_data:
			password = validated_data["password"]
		elif 'fb_userId' in validated_data:
			fb_userId = validated_data["fb_userId"]
		elif 'google_userId' in validated_data:
			google_userId = validated_data["google_userId"]
		elif 'linkedin_token' in validated_data:
			linkedin_token = validated_data["linkedin_token"]
			url = 'https://www.linkedin.com/oauth/v2/accessToken'
			linkedinRedirectUri = linkedinSniffRedirectUri
			if isLocalHost == True:
				linkedinRedirectUri = linkedinSniffLocalHostRedirectUri
			payload = {'grant_type': 'authorization_code', 'client_secret': linkedinClientSecret, 'client_id': linkedinClientId, 'code': linkedin_token, 'redirect_uri': linkedinRedirectUri}
			json = requests.get(url, params=payload).json()
			if 'access_token' in json:				
				linkedin_real_token = json["access_token"]
			else:
				raise ValidationError("Problem with Linkedin authentication.")
				return
		if password != "":
			password_is_valid = validatePassword(password)
			if password_is_valid != True:
				raise ValidationError(password_is_valid)
				return
			validated_data["password"] = crypt_password(validated_data["password"])
		elif fb_userId == "" and google_userId == "" and linkedin_real_token == "":
			raise ValidationError("Password is required to create an account.")
			return
		return User.objects.create(**validated_data)

class UserLoginSerializer(ModelSerializer):

	token = serializers.CharField(allow_blank=True, read_only=True)
	first_name = serializers.CharField(allow_blank=True, read_only=True)
	last_name = serializers.CharField(allow_blank=True, read_only=True)
	displayname = serializers.CharField(allow_blank=True, read_only=True)
	email = serializers.EmailField()
	password = serializers.CharField(allow_blank=True,required=False)
	user_id =  serializers.IntegerField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)

	class Meta:
		model = User
		fields = '__all__'
		extra_kwargs = {"password": {"write_only":True}}

	def validate(self, data):
		user_obj = None
		email = data.get("email", None)
		if not email:
			raise ValidationError("Email is required to login.")
		
		user = User.objects.filter( Q(email=email) ).distinct()
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("This email is not valid.")
		
		password = ""
		fb_userId = ""
		fb_token = ""
		google_token = ""
		google_userId = ""
		linkedin_token = ""
		linkedin_real_token = ""

		if 'password' in data:
			password = data["password"]
		elif 'fb_token' in data:
			if 'fb_userId' in data:
				fb_token = data["fb_token"]
				fb_userId = data["fb_userId"]
				#post request to https://graph.facebook.com/app/?fb_token
				url = 'https://graph.facebook.com/app/?access_token='+fb_token # Set destination URL here
				json = requests.get(url).json()
				if 'id' in json:
					appId = json["id"]
					if matchAppId(appId) == False:
						raise ValidationError("Problem with Facebook authentication. If you don't have an account, sign up.")
						return
					#post to https://graph.facebook.com/me?fields=id&access_token= fb_token
					url = 'https://graph.facebook.com/me?fields=id&access_token='+fb_token # Set destination URL here
					json2 = requests.get(url).json()
					if json2["id"] != fb_userId:
						raise ValidationError("Problem with Facebook login. If you don't have an account, sign up.")
						return
				else:
					raise ValidationError("Problem with Facebook authentication.")
			else: 
				raise ValidationError("Problem with Facebook authentication.")
		elif 'google_token' in data:
			google_token = data["google_token"]
			google_userId = verifyGoogle(google_token)
			if google_userId != data["google_userId"]: 
				raise ValidationError("Problem with Google authentication.")

		elif 'linkedin_token' in data:
			linkedin_token = data["linkedin_token"]
			print
			url = 'https://www.linkedin.com/oauth/v2/accessToken'
			linkedinRedirectUri = linkedinSniffRedirectUri
			if isLocalHost == True:
				linkedinRedirectUri = linkedinSniffLocalHostRedirectUri
			payload = {'grant_type': 'authorization_code', 'client_secret': linkedinClientSecret, 'client_id': linkedinClientId, 'code': linkedin_token, 'redirect_uri': linkedinRedirectUri}
			json = requests.get(url, params=payload).json()
			if 'access_token' in json:				
				linkedin_real_token = json["access_token"]
			else:
				raise ValidationError("Problem with Linkedin authentication.")
		#if user is logging in with facebook
		if user_obj:
			if not user_obj.check_authentication(password,fb_userId,google_userId,linkedin_real_token):
				raise ValidationError("Incorrect credentials, please try again.")
		if user_obj.get_token() == False and fb_userId == False and google_userId == False and linkedin_real_token == False:
			raise ValidationError("Problem with login, please try again.")
		token = ""
		if user_obj.get_token() != False:
			token = user_obj.get_token()
		returnData = dict()
		returnData["token"] = token
		returnData["email"] = email
		returnData["first_name"] = user_obj.first_name
		returnData["last_name"] = user_obj.last_name
		returnData["displayname"] = user_obj.displayname
		returnData["created_at"] = user_obj.created_at
		returnData["user_id"] = user_obj.user_id
		# data["fb_userId"] = user_obj.fb_userId
		returnData["google_userId"] = user_obj.google_userId
		returnData["linkedin_token"] = user_obj.linkedin_token
		returnData["password"] = user_obj.password
		return returnData


























