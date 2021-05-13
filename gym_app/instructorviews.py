from datetime import date
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from gym_app import models
from gym_app.forms import AddDietPlan
from gym_app.models import UserHealth, DietPlan, Attendance, Register, FirstAid


def add_health(request):
    name = Register.objects.filter(role='Customer')
    if request.method == 'POST':
        nam = request.POST.get('cname')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        issue = request.POST.get('issue')
        medicine = request.POST.get('medicine')

        health = models.UserHealth()
        health.name = Register.objects.filter(role='Customer').get(user_id=nam)
        health.height = height
        health.weight = weight
        health.health_issue = issue
        health.medicine_consumption = medicine
        health.instructor = Register.objects.filter(role='Instructor').get(user=request.user)
        health.save()
        messages.info(request,'User health Detail Added')
        return redirect('add_health')

    return render(request, 'instructor/add_health_detail.html', {'names': name})


def view_health_issue(request):
    i = Register.objects.filter(role='Instructor').get(user=request.user)
    detail = UserHealth.objects.filter(instructor=i)
    return render(request, 'instructor/view_health_detail.html', {'details': detail})


def edit_health_issue(request, id):
    detail = UserHealth.objects.get(id=id)
    if request.method == 'POST':
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        issue = request.POST.get('issue')
        medicine = request.POST.get('medicine')

        detail.height = height
        detail.weight = weight
        detail.health_issue = issue
        detail.medicine_consumption = medicine
        detail.save()
        return redirect('view_health')

    return render(request, 'instructor/edit_health_detail.html', {'details': detail})


def add_diet(request):
    form = AddDietPlan()
    if request.method == 'POST':
        form = AddDietPlan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Diet Plan Added Successfully')
            return redirect('view_diet')
    return render(request, 'instructor/add_diet.html', {'form': form})


def view_diet(request):
    diet = DietPlan.objects.all()
    return render(request, 'instructor/view_diet.html', {'diets': diet})


def edit_diet(request, id):
    diet = DietPlan.objects.get(id=id)
    form = AddDietPlan(instance=diet or None)
    if request.method == 'POST':
        form = AddDietPlan(request.POST or None, request.FILES or None, instance=diet or None)
        if form.is_valid():
            form.save()
            messages.info(request, 'DietPlan Updated Successfully')
            return redirect('view_diet')
    return render(request, 'instructor/edit_diet.html', {'form': form})


def delete_diet(request, id):
    diet = DietPlan.objects.get(id=id)
    if request.method == 'POST':
        diet.delete()
        return redirect('view_diet')
    return render(request, 'instructor/delete_diet.html')


def view_firstaid_instructor(request):
    firstaid = FirstAid.objects.all()
    return render(request, 'instructor/view_firstaid_instructor.html', {'firstaids': firstaid})


def add_attendance(request):
    name = models.Register.objects.filter(role='Customer')
    return render(request, 'instructor/add_attendance.html', {'names': name})


def mark(request, id):
    user = Register.objects.get(id=id)
    att = Attendance.objects.filter(name=user,date=date.today())
    if att.exists():
        messages.info(request,"Today's Attendance Already marked for this User ")
        return redirect('add_attendance')
    else:
        if request.method == 'POST':
            attndc = request.POST.get('attendance')
            attendance = Attendance()
            attendance.attendance = attndc
            attendance.name = user
            attendance.date = date.today()
            attendance.save()
            return redirect('add_attendance')
    return render(request, 'instructor/mark_attendance.html')


def view_attendance(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request, 'instructor/view_attendance_instructor.html', {'attendances': attendance})


def day_attendance(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendances': attendance,
        'date': date
    }
    return render(request, 'instructor/day_attendance.html', context)
