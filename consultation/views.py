from django.shortcuts import render

# Create your views here.

# from base.models import Appointment


def appointment_book(request):

    if request.method == "POST":
        time = request.POST['timing']
        date = request.POST['date']
        doctor = request.POST['doctor']

        print(time)
        print(date)
        print(doctor)
        student = Student.objects.filter(student_id='1')
        teacher = Teachers.objects.filter(teacher_id = '1')
        # Appointment.objects.create(student_id = student, teacher_id = teacher)
    return render(request,'student_book_appointment.html')
