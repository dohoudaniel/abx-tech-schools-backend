from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet, ParentStudentViewSet

router = DefaultRouter()
router.register(r'', ParentViewSet, basename='parent')
router.register(r'links', ParentStudentViewSet, basename='parent-student')

urlpatterns = [
    path('', include(router.urls)),
]
