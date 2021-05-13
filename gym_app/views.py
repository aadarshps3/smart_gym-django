from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from gym_app.forms import InstructorSignUpForm, PhysicianSignUpForm, CustomerSignUpForm, LoginRegister
from gym_app.models import User


def index(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def batches(request):
    return render(request, 'home/schedule.html')


def instructor(request):
    return render(request, 'home/instructor.html')


def contact(request):
    return render(request, 'home/contact-us.html')


def service(request):
    return render(request, 'home/service.html')


def gallery(request):
    return render(request, 'home/gallery.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_page')
            elif user.is_customer:
                return redirect('user_page')
            elif user.is_instructor:
                return redirect('instructor_page')
            elif user.is_physician:
                return redirect('physician_page')
        else:
            messages.info(request, 'Invalid Credentials')

    return render(request, 'login.html')


def admin_page(request):
    return render(request, 'admintemp/admin_home.html')


def instructor_register(request):
    login_form = LoginRegister()
    instructor_form = InstructorSignUpForm()

    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        instructor_form = InstructorSignUpForm(request.POST, request.FILES)
        if login_form.is_valid() and instructor_form.is_valid():
            user = login_form.save(commit=False)
            user.is_instructor = True
            user.save()
            c = instructor_form.save(commit=False)
            c.user = user
            c.role = 'Instructor'
            c.save()
            messages.info(request, 'Instructor Registered Successfully')
            return redirect('instructor_register')



    return render(request, 'admintemp/instructor_register.html',
                  {'login_form': login_form, 'instructor_form': instructor_form})


def instructor_page(request):
    return render(request, 'instructor/instructor_home.html')


def physician_register(request):
    login_form = LoginRegister()
    physician_form = PhysicianSignUpForm()

    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        physician_form = PhysicianSignUpForm(request.POST, request.FILES)
        if login_form.is_valid() and physician_form.is_valid():
            user = login_form.save(commit=False)
            user.is_physician = True
            user.save()
            c = physician_form.save(commit=False)
            c.user = user
            c.role = 'Physician'
            c.save()
            messages.info(request, 'Physician Registered Successfully')
            return redirect('admin_page')

    return render(request, 'admintemp/physician_register.html',
                  {'login_form': login_form, 'physician_form': physician_form})


def physician_page(request):
    return render(request, 'physician/physician_home.html')


def customer_register(request):
    login_form = LoginRegister()
    customer_form = CustomerSignUpForm()

    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        customer_form = CustomerSignUpForm(request.POST, request.FILES)
        if login_form.is_valid() and customer_form.is_valid():
            user = login_form.save(commit=False)
            user.is_customer = True
            user.save()
            c = customer_form.save(commit=False)
            c.user = user
            c.role = 'Customer'
            c.save()
            messages.info(request, 'Customer Registered Successfully')
            return redirect('view_user')

        else:
            login_form = LoginRegister()
            customer_form = CustomerSignUpForm()

    return render(request, 'admintemp/customer_register.html',
                  {'login_form': login_form, 'customer_form': customer_form})


def logout_view(request):
    logout(request)
    return redirect('/')


def user_page(request):
    return render(request, 'usertemplates/user_home.html')
