from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
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
    url(r'^dologin/$', views.dologin),
    url(r'^insert/$', views.insert_grade),
]
