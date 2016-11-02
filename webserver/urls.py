"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from sniff import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/users/$', views.ListUsers.as_view()),
    #requires Authorization - user token
    url(r'^api/user/(?P<pk>[0-9]+)$', views.ListUser.as_view()),
    url(r'^api/login/$', views.ListLogin.as_view()),
    url(r'^api/login/linkedin/$', views.ListLogin.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)