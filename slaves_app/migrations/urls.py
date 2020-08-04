from django.urls import path

from django.contrib import admin
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from slaves_app import views

router = routers.SimpleRouter()

router.register(r'Slaves', views.SlaveViewSet, basename="machines_list")
router.register(r'Setting', views.SettingViewSet, basename="main_packs_list")
router.register(r'Technicians', views.TechnicianViewSet, basename="technicians_list")