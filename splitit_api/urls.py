from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
from . import views

schema_view = get_swagger_view(title='SplitIT API')
router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'expense_groups', views.ExpenseGroupsViewSet, basename='expense_groups')
router.register(r'expenses', views.ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
    path(r'^swagger/$', schema_view)
]
