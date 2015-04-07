from django.conf.urls import url
from bands import views

urlpatterns = [url(r'^cvlist/$', views.cvlist, name='cvlist'),
               url(r'^ws/(?P<org>\w+)/$', views.cytobands_ws, name='cytobands_ws'),
               url(r'^(?P<org>[human|mouse]\w+)/$', views.cytobands, name='cytobands'),
               url(r'^$', views.cytobandsHuman, name='cytobandsHuman'),
               ]
