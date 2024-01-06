from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

schema_view = get_swagger_view(title='SplitIT API')
router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'^swagger/$', schema_view)
]
