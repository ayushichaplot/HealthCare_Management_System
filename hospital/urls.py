"""hospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from furst import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(
        r'^api/v1/patients/(?P<pk>[0-9]+)$',
        views.get_delete_update_patient,
        name='get_delete_update_patient'
    ),
    url(
        r'^api/v1/patients/$',
        views.get_post_patients,
        name='get_post_patients'
    ),
    url(
        r'^api/v1/visits/$',
        views.get_post_visits,
        name='get_post_visits'
    ),
    url(
        r'^api/v1/visits/(?P<pk>[0-9]+)$',
        views.get_delete_update_visit,
        name='get_delete_update_visit'
    ),

]
