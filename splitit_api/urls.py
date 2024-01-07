from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="SplitIT API",
      default_version='v1',
      description="API description for SplitIT app",
      contact=openapi.Contact(email="smofficial462@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[],
)
router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'expense_groups', views.ExpenseGroupsViewSet, basename='expense_groups')
router.register(r'expenses', views.ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/', views.AuthViewSet.as_view(), name='auth'),
    path('', include(router.urls)),
]
