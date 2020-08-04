from rest_framework import routers
from slaves_app import views

router = routers.SimpleRouter()

router.register(r'Slaves', views.SlaveViewSet, basename="Slaves_list")
router.register(r'Setting', views.SettingViewSet, basename="Setting_list")
router.register(r'SensorValueType', views.SensorValueTypeViewSet, basename="SensorValueType_list")
