from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from gym_app import models
from gym_app.forms import AddBatch, AddInstructor, AddBill, AddService, AddEquipment, ReplyForm
from gym_app.models import Services, Equipment, Complaints, Batch, Register, Instructor, Attendance
from .forms import *


def user_view(request):
    user = models.Register.objects.filter(role="Customer")
    return render(request, 'admintemp/user_view.html', {'users': user})


def staff_view(request):
    staff = Register.objects.exclude(role='Customer')
    return render(request, 'admintemp/view_staff.html', {'staffs': staff})


def delete_staff(request, id):
    staff = Register.objects.get(id=id)
    u = User.objects.get(register=staff)
    if request.method == 'POST':
        u.delete()
        return redirect('view_staff')
    return render(request, 'admintemp/delete_staff.html')


def approve_user(request, user_id):
    user = Register.objects.get(user_id=user_id)
    user.status = 1
    user.save()
    return HttpResponseRedirect(reverse('view_user'))


def add_batch(request):
    form = AddBatch()
    form2 = PhysicianSignUpForm()
    form3 = LoginRegister()

    if request.method == 'POST':
        form = AddBatch(request.POST)
        if form.is_valid():
            bat = form.save(commit=False)
            batch_qs = Batch.objects.filter(batch_name=bat.batch_name)
            if batch_qs.exists():
                messages.info(request, 'A Batch with this name already exists')
            else:
                bat.save()

                messages.info(request, 'Batch Added Successfully')
                return redirect('add_batch')
    return render(request, 'admintemp/add_batches.html', {'form': form, 'form2': form2, 'form3': form3})


def add_instructor(request):
    form = AddInstructor()
    if request.method == 'POST':
        form = AddInstructor(request.POST)
        if form.is_valid():
            i = form.save(commit=False)
            if Instructor.objects.filter(batch=i.batch).exists():
                messages.info(request, 'Instructor already added for this batch')
            else:
                i.save()
                messages.info(request, 'Instructor Added Successfully')
                return redirect('add_instructor')
    return render(request, 'admintemp/add_instructor.html', {'form': form})


def view_batches(request):
    batch = Batch.objects.all()
    instructor = Instructor.objects.all()
    return render(request, 'admintemp/view_batches.html',{'batch':batch,'instructor':instructor})


def view_attendance_admin(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request, 'admintemp/view_attendance_admin.html', {'attendances': attendance})


def day_attendance_admin(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendances': attendance,
        'date': date
    }
    return render(request, 'admintemp/day_attendance.html', context)


def bill(request):
    form = AddBill()
    if request.method == 'POST':
        form = AddBill(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            if b.present_days == 0:
                messages.info(request, "User Haven't Attended gym during this period")
            else:
                b.save()
                messages.info(request, 'Bill Added Successfully')
                return redirect('view_bill')
    else:
        form = AddBill()

    return render(request, 'admintemp/generate_bill.html', {'form': form})


# AJAX
def load_bill(request):
    customer_id = request.GET.get('customerId')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    customer = Register.objects.get(id=customer_id)
    present_days = Attendance.objects.filter(name=customer, date__range=[from_date, to_date]).count()
    amount = present_days * 100
    data = {
        'present_days': present_days,
        'amount': amount

    }

    return JsonResponse(data)


def view_bill(request):
    bill = models.Bill.objects.all()
    return render(request, 'admintemp/view_payment_details.html', {'bills': bill})


def add_service(request):
    form = AddService()
    if request.method == 'POST':
        form = AddService(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'service Added Successfully')
            return redirect('view_service')

    return render(request, 'admintemp/add_service.html', {'form': form})


def view_service(request):
    service = Services.objects.all()
    return render(request, 'admintemp/view_services.html', {'services': service})


def edit_service(request, id):
    service = Services.objects.get(id=id)
    form = AddService(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid():
        form.save()
        messages.info(request, 'service Updated Successfully')
        return redirect('view_service')

    return render(request, 'admintemp/edit_service.html', {'form': form})


def delete_service(request, id):
    service = Services.objects.get(id=id)
    if request.method == 'POST':
        service.delete()
        return redirect('view_service')
    return render(request, 'admintemp/delete_service.html')


def add_equipment(request):
    form = AddEquipment()
    if request.method == 'POST':
        form = AddEquipment(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Equipment Added Successfully')
            return redirect('view_equipment')
    return render(request, 'admintemp/add_equipment.html', {'form': form})


def view_equipment(request):
    equipment = Equipment.objects.all()
    return render(request, 'admintemp/view_equipment.html', {'equipments': equipment})


def edit_equipment(request, id):
    equipment = Equipment.objects.get(id=id)

    form = AddEquipment(instance=equipment or None)
    if request.method == 'POST':
        form = AddEquipment(request.POST or None, request.FILES or None, instance=equipment or None)
        if form.is_valid():
            form.save()
            messages.info(request, 'Equipment Updated Successfully')
            return redirect('view_equipment')
    return render(request, 'admintemp/edit_equipment.html', {'form': form})


def delete_equipment(request, id):
    equipment = Equipment.objects.get(id=id)
    if request.method == 'POST':
        equipment.delete()
        return redirect('view_equipment')
    return render(request, 'admintemp/delete_equipment.html')


def view_complaint(request):
    complaint = Complaints.objects.all()
    return render(request, 'admintemp/view_complaint.html', {'complaints': complaint})


def reply_complaint(request, id):
    ct = Complaints.objects.get(id=id)
    form = ReplyForm()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.cleaned_data.get('reply')

            ct.reply = reply
            ct.save()
            messages.info(request, 'Reply Send Successfully')
            return redirect('view_complaint')
    return render(request, 'admintemp/reply_complaint.html', {'form': form})


def delete_complaint(request, id):
    complaint = Complaints.objects.get(id=id)
    if request.method == 'POST':
        complaint.delete()
        return redirect('view_complaint')
    return render(request, 'admintemp/delete_complaint.html')


# AJAX
def load_batch_time(request):
    batch_name_id = request.GET.get('batch_id')
    time = Batch.objects.filter(batch_id=batch_name_id, approval_status=1).all()

    return JsonResponse(list(time.values('id', 'batch_time')), safe=False)
