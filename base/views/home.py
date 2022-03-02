from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Students,Teachers

from itertools import chain
from datetime import timedelta, datetime
from django.utils import timezone
def landing_page(request):
    return render(request,'base/gifted/index.html')

def about_us(request):
    return render(request, 'base/gifted/about.html')  

def contact_us(request):
    return render(request, 'base/gifted/contact.html')

def courses(request):
    return render(request, 'base/gifted/courses.html')    

def gifted_prices(request):
    return render(request, 'base/gifted/price.html')

def feedback_form(request):
    return render(request, 'base/gifted/sidebar-right.html')

def gifted_videos(request):
    return render(request, 'base/gifted/videos.html')    

@login_required(login_url='login')
def home(request):
    try :
        student = Students.objects.get(student_id = request.user)
        subscribed = student.student_id.is_subscribed
        freetrial = student.student_id.is_free_trial
        print(12345)
        present = timezone.now()
        if present < student.student_id.expiry_free_trial:
            request.user.is_free_trial = False
            request.user.finished_free_trial = True
            request.user.save()
            freetrial = False

        print(present < student.student_id.expiry_free_trial)
    except Exception as e:
        print(e)
        subscribed = True
        freetrial = False
    
    if (not subscribed and not freetrial):
        return redirect('paymenthome')
    else:    
        teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
        student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
        teachers_all = Teachers.objects.all()
        mappings = chain(teacher_mapping,student_mapping) 
        try:
            student = Students.objects.get(student_id = request.user)
        except Exception as e:
            student = None
        try:
            teacher = Teachers.objects.get(teacher_id = request.user)
        except Exception as e:
            teacher = None
        is_student = 0
        if teacher is None:
            is_student = 1
                            
        return render(request,'base/home.html',{'mappings':mappings,'teachers_all':teachers_all,'is_student':is_student}) 