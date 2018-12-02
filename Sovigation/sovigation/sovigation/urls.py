"""sovigation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from service import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^assignment/$', views.assignment),
    url(r'^board$', views.board),
    url(r'^contact$', views.contact),
    url(r'^food$', views.food),
    url(r'^grade$', views.grade),
    url(r'^index$', views.index),
    url(r'^lib$', views.lib),
    url(r'^about$', views.about),
    url(r'^myservice$', views.myservice),
    url(r'^todo$', views.todo),
]
