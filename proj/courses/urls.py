from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course-list'),
    path('create/', views.course_create, name='course-create'),
    path('<int:pk>/', views.course_detail, name='course-detail'),
    path('<int:pk>/update/', views.course_update, name='course-update'),
    path('<int:pk>/delete/', views.course_delete, name='course-delete'),
    path('enrollments/', views.enrollment_list, name='enrollment-list'),
    path('enrollments/create/', views.enrollment_create, name='enrollment-create'),
    path('enrollments/<int:pk>/update/', views.enrollment_update, name='enrollment-update'),
    path('enrollments/<int:pk>/delete/', views.enrollment_delete, name='enrollment-delete'),
]