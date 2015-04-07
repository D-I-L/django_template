from django.conf.urls import url
from gene import views

urlpatterns = [url(r'^(?P<gene>[-\w]+)/$', views.gene_page, name='gene_page'),
               ]
