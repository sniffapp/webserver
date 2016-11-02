# python manage.py runserver
# python manage.py makemigrations
# python manage.py migrate
# python manage.py shell
# http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
# {
# "first_name": "Andrea",
# "last_name": "Ferrando",
# "email": "andrea.ferrando@icloud.com",
# "password": "mypsw"
# }

# https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#Instances:search=i-09d2a720ebc47c000;sort=tag:Name
# http://52.211.152.199/
# ssh -i sniff_webserver.pem ubuntu@52.211.152.199
# ssh -i "sniff_webserver.pem" ubuntu@ec2-52-212-145-249.eu-west-1.compute.amazonaws.com

# http://agiliq.com/blog/2014/08/deploying-a-django-app-on-amazon-ec2-instance/

# http://sniff.us-west-2.elasticbeanstalk.com/

import hashlib
from oauth2client import client, crypt

debug_beta = True
fbSniffAppId = "284344261951594"
fbSniffBetaAppId = "676580649156001"
googleSniffIOSClientId = "672735175799-07jpi7dr11iq8ehlh7ps8i3131c4dtnm.apps.googleusercontent.com"
googleSniffBetaIOSClientId = "506586701904-5ndfiutu8ro05lkuvm0pqiv0feuv40iv.apps.googleusercontent.com"

def crypt_password(raw_password):
	if raw_password is None:
		return False
	else:
		return hashlib.md5(raw_password).hexdigest()


def validatePassword(password):
    if len(password) < 6:
        return "Password must have at least 6 characters"
    return True

def matchAppId(id):
	if id == fbSniffBetaAppId or id == fbSniffAppId:
		return True
	return False

def verifyGoogle(token):
	CLIENT_ID = googleSniffIOSClientId
	APPS_DOMAIN_NAME = ""
	if debug_beta:
		CLIENT_ID = googleSniffBetaIOSClientId
		APPS_DOMAIN_NAME = ""
	try:
		idinfo = client.verify_id_token(token, CLIENT_ID)
		print("\n\n\n")
		print(idinfo)
		print("\n\n\n")
		# If multiple clients access the backend server:
		if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
			# if idinfo['aud'] not in [googleSniffIOSClientId]:
			raise crypt.AppIdentityError("Unrecognized client.")
		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
			raise crypt.AppIdentityError("Wrong issuer.")
		if idinfo['hd'] != APPS_DOMAIN_NAME:
			raise crypt.AppIdentityError("Wrong hosted domain.")
	except crypt.AppIdentityError:
		raise ValidationError("Problem with Google login.")
	userid = idinfo['sub']
	return userid















