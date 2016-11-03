__author__ = 'tbartel'
from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^$', index),
    url(r'^autocomplete/$', autocomplete),
]