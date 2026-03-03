import datetime
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import Attendance
from courses.models import Course
from students.models import Student
from .forms import AttendanceForm

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'teacher'

@login_required
def attendance_list(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
def mark_attendance(request, course_id):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can mark attendance.")

    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.filter(enrollments__course=course)

    date_str = request.GET.get('date')
    if date_str:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = datetime.date.today()

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')

            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    course=course,
                    defaults={'status': status}
                )

        messages.success(request, "Attendance marked successfully!")
        return redirect('attendance-list')

    attendance_records = Attendance.objects.filter(course=course, date=date)
    attendance_dict = {a.student_id: a.status for a in attendance_records}

    students_with_status = []
    for student in students:
        students_with_status.append({
            'student': student,
            'current_status': attendance_dict.get(student.id, 'present')
        })

    return render(request, 'attendance/mark_attendance.html', {
        'course': course,
        'students_with_status': students_with_status,
        'date': date,
    })

@login_required
def attendance_update(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can update attendance.")
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance-list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/attendance_form.html', {'form': form, 'action': 'Update'})

@login_required
def attendance_delete(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can delete attendance.")
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance-list')
    return render(request, 'attendance/attendance_delete.html', {'attendance': attendance})


@login_required
def export_attendance_txt(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can export attendance.")

    attendances = Attendance.objects.select_related('student', 'course').all()
    if not attendances:
        return redirect('attendance-list')

    content = "ATTENDANCE REPORT\n"
    content += "=" * 50 + "\n\n"

    for a in attendances:
        student_name = a.student.user.get_full_name() or a.student.user.username
        content += f"Student: {student_name}\n"
        content += f"Course: {a.course.name}\n"
        content += f"Status: {a.get_status_display()}\n"
        content += "-" * 30 + "\n"

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    file_name = "attendance_report.txt"

    try:
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=file_name,
            Body=content.encode('utf-8'),
            ContentType='text/plain'
        )

        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

        return HttpResponse(
            f"<h2>Upload Successful</h2>"
            f"<a href='{file_url}' target='_blank'>Download File</a>"
        )

    except Exception as e:
        return HttpResponse(f"Upload Failed<br>{str(e)}")