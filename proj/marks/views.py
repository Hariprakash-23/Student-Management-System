from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Exam, Marks
from .forms import ExamForm, MarksForm
import boto3
from django.conf import settings

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'teacher'


@login_required
def exam_list(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    exams = Exam.objects.all()
    return render(request, 'marks/exam_list.html', {'exams': exams})

@login_required
def exam_create(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can create exams.")

    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()  

            sns = boto3.client(
                "sns",
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            message = f"""
New Exam Scheduled!

Exam: {exam.name}
Course: {exam.course.name}
Date: {exam.date}
Max Marks: {exam.max_marks}
"""
            sns.publish(
                TopicArn=settings.SNS_TOPIC_ARN,
                Subject="New Exam Scheduled",
                Message=message
            )

            return redirect('exam-list')  

    else:
        form = ExamForm()

    return render(request, 'marks/exam_form.html', {'form': form, 'action': 'Create'})
@login_required
def exam_update(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can update exams.")
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam-list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'marks/exam_form.html', {'form': form, 'action': 'Update'})

@login_required
def exam_delete(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can delete exams.")
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam-list')
    return render(request, 'marks/exam_delete.html', {'exam': exam})

# Marks
@login_required
def marks_list(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Access denied.")
    marks = Marks.objects.all()
    return render(request, 'marks/marks_list.html', {'marks': marks})

@login_required
def marks_create(request):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can create marks.")
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marks-list')
    else:
        form = MarksForm()
    return render(request, 'marks/marks_form.html', {'form': form, 'action': 'Create'})

@login_required
def marks_update(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can update marks.")
    mark = get_object_or_404(Marks, pk=pk)
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect('marks-list')
    else:
        form = MarksForm(instance=mark)
    return render(request, 'marks/marks_form.html', {'form': form, 'action': 'Update'})

@login_required
def marks_delete(request, pk):
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teachers can delete marks.")
    mark = get_object_or_404(Marks, pk=pk)
    if request.method == 'POST':
        mark.delete()
        return redirect('marks-list')
    return render(request, 'marks/marks_confirm_delete.html', {'mark': mark})