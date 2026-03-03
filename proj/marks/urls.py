from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.exam_list, name='exam-list'),
    path('exams/create/', views.exam_create, name='exam-create'),
    path('exams/<int:pk>/update/', views.exam_update, name='exam-update'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam-delete'),
    path('', views.marks_list, name='marks-list'),
    path('create/', views.marks_create, name='marks-create'),
    path('<int:pk>/update/', views.marks_update, name='marks-update'),
    path('<int:pk>/delete/', views.marks_delete, name='marks-delete'),
]