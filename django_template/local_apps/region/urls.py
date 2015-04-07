from django.conf.urls import url
from region import views

urlpatterns = [url(r'^(?P<region>[-\w]+)/$', views.region_page, name='region_page'),
               ]
