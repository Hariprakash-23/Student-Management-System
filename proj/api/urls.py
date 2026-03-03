from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'marks', views.MarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]