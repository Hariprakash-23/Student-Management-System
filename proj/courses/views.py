from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'teacher'

def is_student(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'student'

# Course
@login_required
def course_list(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def course_create(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can create courses.")
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Create'})

@login_required
def course_update(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can update courses.")
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Update'})

@login_required
def course_delete(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can delete courses.")
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course-list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# Enrollment
@login_required
def enrollment_list(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    enrollments = Enrollment.objects.all()
    return render(request, 'courses/enrollment_list.html', {'enrollments': enrollments})

@login_required
def enrollment_create(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can create enrollments.")
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enrollment-list')
    else:
        form = EnrollmentForm()
    return render(request, 'courses/enrollment_form.html', {'form': form, 'action': 'Create'})

@login_required
def enrollment_update(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can update enrollments.")
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('enrollment-list')
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'courses/enrollment_form.html', {'form': form, 'action': 'Update'})

@login_required
def enrollment_delete(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can delete enrollments.")
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        return redirect('enrollment-list')
    return render(request, 'courses/enrollment_confirm_delete.html', {'enrollment': enrollment})