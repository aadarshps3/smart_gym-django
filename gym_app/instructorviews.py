from datetime import date
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from gym_app import models
from gym_app.forms import AddDietPlan, UserHealthForm
from gym_app.models import UserHealth, DietPlan, Attendance, Register, FirstAid, Batch, Instructor


def add_health(request):
    name = Register.objects.filter(role='Customer')
    form = UserHealthForm()
    if request.method == 'POST':
        form = UserHealthForm(request.POST)
        if form.is_valid():
            health = form.save(commit=False)
            qs = UserHealth.objects.filter(name=health.name)
            if qs.exists():
                messages.info(request, 'Health Detail Already Added for this user')
            else:

                health.instructor=Register.objects.filter(role='Instructor').get(user=request.user)
                health.save()
                messages.info(request,'User health Detail Added')
                return redirect('add_health')

    return render(request, 'instructor/add_health_detail.html', {'form': form})


def view_health_issue(request):
    i = Register.objects.filter(role='Instructor').get(user=request.user)
    detail = UserHealth.objects.filter(instructor=i)
    return render(request, 'instructor/view_health_detail.html', {'details': detail})


def edit_health_issue(request, id):
    detail = UserHealth.objects.get(id=id)
    form = UserHealthForm(instance=detail)
    if request.method == 'POST':
        form = UserHealthForm(request.POST or None,instance=detail or None)
        if form.is_valid():
            form.save()


            messages.info(request,'User health Detail Updated')

            return redirect('view_health')

    return render(request, 'instructor/edit_health_detail.html', {'form': form})


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
    u = Register.objects.get(user=request.user)
    try:

        in_batch = Instructor.objects.filter(instructor=u)[0]
        # print(in_batch,'lllll')
        # print(u.instructor__batch)
        name = Register.objects.filter(role='Customer',required_batch_name=in_batch.batch)
        return render(request, 'instructor/add_attendance.html', {'names': name})
    except:

        return render(request, 'instructor/add_attendance.html', {'names': 'no batch'})


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
    u = Register.objects.get(user=request.user)
    in_batch = Instructor.objects.filter(instructor=u)[0]
    attendance = Attendance.objects.filter(date=date,name__required_batch_name=in_batch.batch)
    context = {
        'attendances': attendance,
        'date': date
    }
    return render(request, 'instructor/day_attendance.html', context)
