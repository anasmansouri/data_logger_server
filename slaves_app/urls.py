from rest_framework import routers
from slaves_app import views
from django.urls import path

router = routers.SimpleRouter()

router.register(r'Slaves', views.SlaveViewSet, basename="Slaves_list")
router.register(r'Setting', views.SettingViewSet, basename="Setting_list")
router.register(r'MemoryZone', views.MemoryZoneViewSet, basename="Memory_Zone_list")
router.register(r'MemoryZoneHistory', views.MemoryZoneHistoryViewSet, basename="Memory_Zone_History_list")

# TODO we have to add something to allow deleting and updating a specefic memory zone . the problem is that the
#  primary key of the memory zone is a double primary key the pk of the slave and the register address of the memory
#  zone router.register(r'MemoryZoneHistory', views.MemoryZoneHistoryViewSet, basename="Memory_Zone_History_list")

''
urlpatterns = [path('salve_search/', views.salve_search),
               path('read_data/', views.read_data)
               # path('<int:slave_pk>/<int:pk>/', views.MemoryZoneViewSet.as_view({'delete':'destroy'}), name="memory_zone_details")
               ]
urlpatterns += router.urls
