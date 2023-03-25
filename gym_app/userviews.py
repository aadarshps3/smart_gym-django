from datetime import date, datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from gym_app import models
from .utils import render_to_pdf
from django.http import HttpResponse
from django.template.loader import get_template

from gym_app.forms import AppointmentForm, AskDoubtForm, ComplaintForm, PayBillForm, BmiCalculation
from gym_app.models import Register, UserHealth, DietPlan, Attendance, Appointment, Equipment, Doubts, \
    Complaints, Bill, User, CreditCard


def view_batch_user(request):
    user = Register.objects.filter(user=request.user)
    return render(request, 'usertemplates/view_batch_user.html', {'users': user})


def view_diet_user(request):
    diet = DietPlan.objects.all()
    return render(request, 'usertemplates/view_diet_user.html', {'diets': diet})


def take_appointment(request):
    form = AppointmentForm()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appo = form.save(commit=False)
            appo.user_name = Register.objects.get(user=request.user)
            appo.save()
            messages.info(request, 'Appointment Requested Successfully')
            return redirect('view_appointment_user')
    return render(request, 'usertemplates/take_appointment.html', {'form': form})


def view_appointment_user(request):
    u = Register.objects.get(user=request.user)
    appointment = Appointment.objects.filter(user_name=u)
    return render(request, 'usertemplates/view_appointment_user.html', {'appointments': appointment})


def view_equipment_user(request):
    equipment = Equipment.objects.all()
    return render(request, 'usertemplates/view_equipment_user.html', {'equipments': equipment})


def ask_doubts(request):
    form = AskDoubtForm()
    if request.method == 'POST':
        form = AskDoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.user_name = Register.objects.get(user=request.user)
            doubt.save()
            messages.info(request, 'Doubt Send Successfully')
            return redirect('view_doubt')
    return render(request, 'usertemplates/ask_doubts.html', {'form': form})


def view_doubt(request):
    u = Register.objects.get(user=request.user)
    doubt = Doubts.objects.filter(user_name=u)
    return render(request, 'usertemplates/view_medical_doubts.html', {'doubts': doubt})


def edit_doubt(request, id):
    doubt = Doubts.objects.get(id=id)
    if request.method == 'POST':
        dt = request.POST.get('doubt')

        doubt.doubts = dt
        doubt.save()
        return redirect('view_doubt')
    return render(request, 'usertemplates/edit_doubt.html', {'doubts': doubt})


def delete_doubt(request, id):
    doubt = Doubts.objects.get(id=id)
    if request.method == 'POST':
        doubt.delete()
        return redirect('view_doubt')
    return render(request, 'usertemplates/delete_doubt.html')


def add_complaint(request):
    form = ComplaintForm()
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.user_name = Register.objects.get(user=request.user)
            comp.save()
            messages.info(request, 'Complaint Send Successfully')
            return redirect('view_complaint_user')
    return render(request, 'usertemplates/add_complaint.html', {'form': form})


def view_complaint_user(request):
    u = Register.objects.get(user=request.user)
    complaint = Complaints.objects.filter(user_name=u)
    return render(request, 'usertemplates/view_complaint_user.html', {'complaints': complaint})


def view_attendance_user(request):
    u = Register.objects.get(user=request.user)
    attendance = Attendance.objects.filter(name=u)
    return render(request, 'usertemplates/view_attendance_user.html', {'attendances': attendance})


def view_bill_user(request):
    u = Register.objects.get(user=request.user)
    bill = Bill.objects.filter(name=u)
    return render(request, 'usertemplates/view_bill_user.html', {'bills': bill})


def pay_bill(request, id):
    bi = Bil  / l.objects.get(id=id)
    form = PayBillForm()
    if request.method == 'POST':
        card = request.POST.get('card')
        c = request.POST.get('cvv')
        da = request.POST.get('exp')
        CreditCard(card_no=card, card_cvv=c, expiry_date=da, bill=bi).save()
        bi.status = 1
        bi.save()
        messages.info(request, 'Bill Paid  Successfully')
        return redirect('bill_history')

        # form = PayBillForm(request.POST)
        # if form.is_valid():
        #     pay = form.save(commit=False)
        #     pay.bill = bi
        #     pay.save()
        #     bi.status = 1
        #     bi.save()

    return render(request, 'usertemplates/pay_bill.html', )


def pay_in_direct(request, id):
    bi = Bill.objects.get(id=id)
    bi.status = 2
    bi.save()
    messages.info(request,'Choosed to Pay Fee Direct in office')
    return redirect('bill_history')


def bill_history(request):
    u = Register.objects.get(user=request.user)
    bill = Bill.objects.filter(name=u, status__in=[1,2])

    return render(request, 'usertemplates/view_bill_history.html', {'bills': bill})


def get_invoice(request, id):
    u = Register.objects.get(user=request.user)
    bill = Bill.objects.get(id=id)
    template = get_template('usertemplates/invoice.html')
    html = template.render({'data': bill})

    pdf = render_to_pdf('usertemplates/invoice.html', {'data': bill})

    return HttpResponse(pdf, content_type='application/pdf')


def view_invoice(request, id):
    u = Register.objects.get(user=request.user)
    bill = Bill.objects.filter(id=id)
    return render(request, 'usertemplates/invoice.html', {'data': bill})


def view_transformation(request):
    u = Register.objects.get(user=request.user)
    trasnformation = UserHealth.objects.filter(name=u)[:1]
    return render(request, 'usertemplates/view_transformation.html', {'trasnformations': trasnformation})


def bmi(request):
    form = BmiCalculation()
    if request.method == 'POST':
        form = BmiCalculation(request.POST)
        if form.is_valid():
            height = form.cleaned_data.get('height')
            weight = form.cleaned_data.get('weight')
            user_bmi = (float(weight) / float(height) / float(height)) * 10000
            bmi = round(user_bmi, 1)
            return redirect('view_bmi', bmi)
    return render(request, 'usertemplates/bmi.html', {'form': form})


def view_bmi(request, bmi):
    user_bmi = float(bmi)
    return render(request, 'usertemplates/view_bmi.html', {'user_bmi': user_bmi})


def drop_gym(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.info(request, 'Your Account has been Deleted')
        return redirect('login_view')
    return render(request, 'usertemplates/drop_gym.html')
