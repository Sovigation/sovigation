from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^about/$', views.about),
    url(r'^assignment/$', views.assignment),
    url(r'^board/$', views.board),
    url(r'^food/$', views.food),
    url(r'^grade/$', views.grade),
    url(r'^lib/$', views.lib),
    url(r'^login/$', views.login),
    url(r'^myService/$', views.myService),
    url(r'^to_do/$', views.to_do),
]
