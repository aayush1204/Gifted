from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from ..decorators import login_excluded
from ..forms import UserAuthenticationForm,UserRegisterationForm
from ..models import Students,Teachers
from itertools import chain

@login_excluded('home')
def register_view(request):
    if request.method=="POST":
        form=UserRegisterationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user_name=form.cleaned_data.get('username')
            login(request,user)
            return redirect('paymenthome')
        else:
            return render(request,'base/register.html',{'form':form})
    form=UserRegisterationForm()
    return render(request,'base/register.html',{'form':form})

@login_excluded('home')  
def login_view(request):
    if request.method=="POST":
        form=UserAuthenticationForm(request=request,data=request.POST)
        print(form)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            print(user_name)
            print(password)
            user=authenticate(username=user_name,password=password)
            if user!=None:
                login(request,user)
                try :
                    student = Students.objects.get(student_id = request.user)
                    subscribed = student.student_id.is_subscribed
                    freetrial = student.student_id.is_free_trial
                    
                except Exception as e:
                    subscribed = True
                    freetrial = False
                    
                if (not subscribed and not freetrial) :
                    return redirect('paymenthome')
                else:    
                    return redirect('home')
        else:
            return render(request,'base/login.html',{'form':form})
    form=UserAuthenticationForm() 
    return render(request,'base/login.html',{'form':form}) 

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')