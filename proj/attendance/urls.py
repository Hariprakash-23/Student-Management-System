from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance-list'),
    path('mark/<int:course_id>/', views.mark_attendance, name='mark-attendance'),
    path('<int:pk>/update/', views.attendance_update, name='attendance-update'),
    path('<int:pk>/delete/', views.attendance_delete, name='attendance-delete'),
    path('export-s3/', views.export_attendance_txt, name='attendance-export-s3'),
]