from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Student
from .forms import StudentForm
from courses.models import Course
from courses.models import Enrollment
from attendance.models import Attendance
from marks.models import Marks
from django.utils import timezone
from marks.models import Exam

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'teacher'

def is_student(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'student'

@login_required
def teacher_dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_attendances = Attendance.objects.count()
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_attendances': total_attendances
    }
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    return render(request, 'students/teacher_dashboard.html',context)

@login_required
def student_dashboard(request):
    if not is_student(request.user):
        return HttpResponseForbidden("Access denied.")
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return render(request, 'students/student_dashboard.html',
                      {'error': 'Student profile not found. Please contact administrator.'})

    enrollments = Enrollment.objects.filter(student=student)
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    marks = Marks.objects.filter(student=student)

    enrolled_course_ids = enrollments.values_list('course_id', flat=True)
    upcoming_exams = Exam.objects.filter(
        course_id__in=enrolled_course_ids,
        date__gte=timezone.now().date()
    ).order_by('date')

    return render(request, 'students/student_dashboard.html', {
        'student': student,
        'enrollments': enrollments,
        'attendances': attendances,
        'marks': marks,
        'upcoming_exams': upcoming_exams,   # <-- pass to template
    })


@login_required
def student_list(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can view all students.")
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {
        'students': students,
        'is_teacher': True,
    })

@login_required
def student_detail(request, reg_no):   
    student = get_object_or_404(Student, Reg_no=reg_no)
    if is_student(request.user):
        try:
            user_student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return HttpResponseForbidden("Your student profile is missing.")
        if user_student.Reg_no != student.Reg_no:
            return HttpResponseForbidden("You can only view your own profile.")
    return render(request, 'students/student_detail.html', {
        'student': student,
        'is_teacher': is_teacher(request.user),
    })

@login_required
def student_create(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can create students.")
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Create'})

@login_required
def student_update(request, reg_no):   
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can update students.")
    student = get_object_or_404(Student, Reg_no=reg_no)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Update'})

@login_required
def student_delete(request, reg_no):   
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can delete students.")
    student = get_object_or_404(Student, Reg_no=reg_no)
    if request.method == 'POST':
        student.delete()
        return redirect('student-list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})