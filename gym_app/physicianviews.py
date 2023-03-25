from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from gym_app import models
from gym_app.forms import FirstAidForm, UserHealthForm, UserHealthUpdateForm, ReplyForm
from gym_app.models import Register, UserHealth, DietPlan, Attendance, FirstAid, Appointment, Doubts


def consultation_time(request):
    time = Register.objects.filter(user=request.user)

    return render(request,'physician/consultation_time.html',{'time':time})
def view_user_health(request):
    detail = UserHealth.objects.all()
    return render(request,'physician/view_health_physician.html',{'details':detail})


def edit_user_health(request, id):
    detail = UserHealth.objects.get(id=id)

    form = UserHealthUpdateForm(instance=detail)
    if request.method == 'POST':
        form = UserHealthUpdateForm(request.POST or None, instance=detail or None)
        if form.is_valid():
            form.save()

            messages.info(request, 'User health Detail Updated')
        return redirect('view_user_health')
    return render(request, 'physician/edit_health_physician.html', {'form': form})




def view_appointment(request):
    i = Register.objects.filter(role='Physician').get(user=request.user)
    appointment = Appointment.objects.filter(physician=i)
    return render(request,'physician/view_appointment_physician.html',{'appointments':appointment})


def approve_appointment(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = 1
    appointment.save()
    return HttpResponseRedirect(reverse('view_appointment'))


def reject_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        appointment.status = 2
        appointment.save()
        return redirect('view_appointment')
    return render(request, 'physician/reject_appointment.html' )


def add_first_aid(request):
    form = FirstAidForm()
    if request.method == 'POST':
        form = FirstAidForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'FirstAid Added Successfully')
            return redirect('view_first_aid')
    return render(request,'physician/add_first_aid.html',{'form':form})


def view_first_aid(request):
    firstaid = FirstAid.objects.all()
    return render(request,'physician/view_first_aid.html',{'firstaids':firstaid})


def edit_first_aid(request,id):
    firstaid = FirstAid.objects.get(id=id)
    form = FirstAidForm(instance=firstaid or None)
    if request.method == 'POST':
        form = FirstAidForm(request.POST or None,instance=firstaid or None)
        if form.is_valid():
            form.save()
            messages.info(request, 'FirstAid Updated Successfully')

            return redirect('view_first_aid')
    return render(request,'physician/edit_first_aid.html',{'form':form})


def delete_first_aid(request,id):
    firstaid = FirstAid.objects.get(id=id)
    if request.method == 'POST':
        firstaid.delete()
        return redirect('view_first_aid')
    return render(request,'physician/delete_first_aid.html')


def view_medicaldoubts_physician(request):
    i = Register.objects.filter(role='Physician').get(user=request.user)
    doubt = Doubts.objects.filter(physician=i)
    return render(request,'physician/view_medical_doubts_physician.html',{'doubts':doubt})


def reply_doubts(request,id):
    doubt = Doubts.objects.get(id=id)
    form = ReplyForm()

    form = ReplyForm()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.cleaned_data.get('reply')
            doubt.reply = reply
            doubt.save()
            return redirect('view_medicaldoubts_physician')

    return render(request,'physician/reply_doubt.html',{'form':form})