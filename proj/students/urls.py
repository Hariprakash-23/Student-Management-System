from django.urls import path
from . import views

urlpatterns = [
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('', views.student_list, name='student-list'),
    path('create/', views.student_create, name='student-create'),
    path('<str:reg_no>/', views.student_detail, name='student-detail'),          
    path('<str:reg_no>/update/', views.student_update, name='student-update'),   
    path('<str:reg_no>/delete/', views.student_delete, name='student-delete'),   
]