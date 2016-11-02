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

fbSniffAppId = "284344261951594"
fbSniffBetaAppId = "676580649156001"

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
