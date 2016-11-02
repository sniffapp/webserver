import binascii
import os
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from .utils import *

class User(models.Model):
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    displayname = models.CharField(max_length=200,blank=True)
    email = models.EmailField(verbose_name="Email",max_length=200, blank=False, unique=True)
    password = models.CharField(verbose_name="Password", max_length=50,blank=True)
    user_id =  models.AutoField(primary_key=True)
    token = models.CharField(max_length=400,blank=True)
    fb_userId = models.CharField(max_length=40,blank=True)
    fb_token = models.CharField(max_length=400,blank=True)
    google_userId = models.CharField(max_length=40,blank=True)
    google_token = models.CharField(max_length=2000,blank=True)
    linkedin_token = models.CharField(max_length=400,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def create(self,validated_data):
    #     print("\n\n\n INSIDE \n\n\n")
    #     print(validated_data)

    def save(self, *args, **kwargs):
        if not self.token and not self.google_token and not self.linkedin_token:
            self.token = self.generate_token()
    	if self.displayname is None or self.displayname == "":
    		self.displayname = self.first_name + " " + self.last_name
    	return super(User,self).save(*args,**kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        # return '%s %s' % (self.first_name, self.last_name)
        return str(self.displayname)

    def check_password(self, raw_password):
    	return self.password == crypt_password(raw_password)

    def get_token(self):
    	if not self.token:
            return False
        return self.token

    def check_authentication(self, password, fb_userId, google_userId, linkedin_token):
    	if password != "":
    		return self.check_password(password)
    	elif fb_userId != "":
    		return self.fb_userId == fb_userId
    	elif google_userId != "":
    		return self.google_userId == google_userId
    	elif linkedin_token != "":
			return self.linkedin_token == linkedin_token
    	return False


