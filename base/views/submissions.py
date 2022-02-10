from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..decorators import student_required
from ..models import Assignments, Students, Submissions
from ..forms import *     
from .. import email

from datetime import datetime

from django.http import HttpResponse
from itertools import chain

@csrf_exempt
@login_required(login_url='login')
@student_required('home')
def submit_assignment_request(request,assignment_id):
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = Students.objects.get(classroom_id=assignment.classroom_id,student_id=request.user.id)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
        submission.submission_file = file_name
        submission.save()
        return JsonResponse({'status':'SUCCESS'})

    except Exception as e:  
        print(str(e))  
        submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
        dt1=datetime.now()
        dt2=datetime.combine(assignment.due_date,assignment.due_time)
        time = timesince(dt1, dt2)
        if time[0]=='0':
            submission.submitted_on_time=False
        submission.save()
        email.submission_done_mail(assignment_id,request.user,file_name)
        return JsonResponse({'status':'SUCCESS'})

def mark_submission_request(request,submission_id,teacher_id):
    if request.method == "POST":
        marks = request.POST['submission_marks']
        assignment_id = request.POST['assignmentid']
        print(assignment_id)
        print(marks)
        print('marks submision')
        print(submission_id)
        submission = Submissions.objects.get(pk=submission_id)
        submission.marks_alloted = marks
        submission.save()
        # email.submission_marks_mail(submission_id,teacher_id,marks)
        # return JsonResponse({'status':'SUCCESS'})

        # return render HttpResponse('<h1>Dniee</h1>')
        # assignment_id = 1
        assignment = Assignments.objects.filter(pk = assignment_id).first()
        submissions = Submissions.objects.filter(assignment_id = assignment_id)
        teachers = Teachers.objects.filter(classroom_id = assignment.classroom_id)
        teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
        student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
        no_of_students = Students.objects.filter(classroom_id=assignment.classroom_id)
        mappings = chain(teacher_mapping,student_mapping)
        return render(request,'base/assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})
