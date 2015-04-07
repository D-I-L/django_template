from django.conf.urls import url
from marker import views

urlpatterns = [url(r'^(?P<marker>[-\w]+)/$', views.marker_page, name='marker_page'),
               ]
