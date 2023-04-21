from django.urls import path, include
from rest_framework import routers

from apiv1 import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
# router.register(r'user', views.UserApi)

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
]
