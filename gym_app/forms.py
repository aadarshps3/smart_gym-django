import datetime
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import PasswordInput, SplitDateTimeWidget
from gym_app.models import User, Register, Batch, Instructor, Bill, Services, Equipment, DietPlan, FirstAid, \
    Appointment, Doubts, Complaints, CreditCard, UserHealth
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class AddBatch(forms.ModelForm):
    batch_time = forms.TimeField(
        widget=TimePicker(
            options={
                'format': 'hh:mm A'
            },
            attrs={
                'append': 'fa fa-clock-o',
                'icon_toggle': True,
            },
        ),
    )

    class Meta:
        model = Batch
        fields = ('batch_name', 'batch_time')


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


gender_choice = (
    ("Male", "Male"),
    ("Female", "Female")
)


class PhysicianSignUpForm(forms.ModelForm):
    consultation_time = forms.TimeField(
        widget=TimePicker(
            options={
                'format': 'hh:mm A'
            },
            attrs={
                'append': 'fa fa-clock-o',
                'icon_toggle': True,
            },
        ),
    )
    phone_no = forms.CharField(validators=[phone_number_validator])
    gender = forms.ChoiceField(choices=gender_choice, required=True, widget=forms.RadioSelect)

    date_of_birth = forms.DateField(widget=DateInput)
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])

    class Meta:
        model = Register
        fields = ('name', 'date_of_birth', 'gender', 'phone_no', 'email', 'address', 'qualification',
                  'consultation_time', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),

        }

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']

        if date >= datetime.date.today():
            raise forms.ValidationError("Invalid Date")
        return date

    def clean_email(self):
        mail = self.cleaned_data['email']
        mail_qs = Register.objects.filter(email=mail)
        if mail_qs.exists():
            raise forms.ValidationError("This email  already registered")
        return mail

    def clean_phone_no(self):
        phone = self.cleaned_data['phone_no']
        phone_qs = Register.objects.filter(phone_no=phone)
        if phone_qs.exists():
            raise forms.ValidationError("This Phone Number already registered")
        return phone


class InstructorSignUpForm(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_number_validator])
    gender = forms.ChoiceField(choices=gender_choice, required=True, widget=forms.RadioSelect)
    date_of_birth = forms.DateField(widget=DateInput)
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])

    class Meta:
        model = Register
        fields = ('name', 'date_of_birth', 'gender', 'phone_no', 'email', 'address', 'qualification', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']

        if date >= datetime.date.today():
            raise forms.ValidationError("Invalid Date")
        return date

    def clean_email(self):
        mail = self.cleaned_data['email']
        mail_qs = Register.objects.filter(email=mail)
        if mail_qs.exists():
            raise forms.ValidationError("This email  already registered")
        return mail

    def clean_phone_no(self):
        phone = self.cleaned_data['phone_no']
        phone_qs = Register.objects.filter(phone_no=phone)
        if phone_qs.exists():
            raise forms.ValidationError("This Phone Number already registered")
        return phone


class CustomerSignUpForm(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_number_validator])
    gender = forms.ChoiceField(choices=gender_choice, required=True, widget=forms.RadioSelect)
    date_of_birth = forms.DateField(widget=DateInput)
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])

    class Meta:
        model = Register
        fields = (
            'name', 'date_of_birth', 'gender', 'phone_no', 'email', 'address', 'occupation', 'required_batch_name',
            'required_batch_time', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']

        if date >= datetime.date.today():
            raise forms.ValidationError("Invalid Date")
        return date

    def clean_email(self):
        mail = self.cleaned_data['email']
        mail_qs = Register.objects.filter(email=mail)
        if mail_qs.exists():
            raise forms.ValidationError("This email  already registered")
        return mail

    def clean_phone_no(self):
        phone = self.cleaned_data['phone_no']
        phone_qs = Register.objects.filter(phone_no=phone)
        if phone_qs.exists():
            raise forms.ValidationError("This Phone Number already registered")
        return phone


class AddInstructor(forms.ModelForm):
    instructor = forms.ModelChoiceField(queryset=Register.objects.filter(role='Instructor'))

    class Meta:
        model = Instructor
        fields = '__all__'


class AddBill(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Register.objects.filter(role='Customer'))
    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)
    due_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Bill
        exclude = ('status', 'paid_on')

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")
        due_date = cleaned_data.get("due_date")

        if (from_date > datetime.date.today()):
            raise forms.ValidationError("Invalid From Date")
        if to_date <= from_date:
            raise forms.ValidationError("Invalid To Date")
        if due_date < datetime.date.today():
            raise forms.ValidationError("Invalid Due Date")
        return cleaned_data


class AddService(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class AddEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'


class AddDietPlan(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = '__all__'


class FirstAidForm(forms.ModelForm):
    class Meta:
        model = FirstAid
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    physician = forms.ModelChoiceField(queryset=Register.objects.filter(role='Physician'))
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Appointment
        fields = ('physician', 'date')

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("Invalid Date")
        return date


class AskDoubtForm(forms.ModelForm):
    physician = forms.ModelChoiceField(queryset=Register.objects.filter(role='Physician'))

    class Meta:
        model = Doubts
        fields = ('physician', 'doubts')


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ('complaint',)


class PayBillForm(forms.ModelForm):
    card_no = forms.CharField(validators=[RegexValidator(regex='^.{16}$', message='Please Enter a Valid Card No')])
    card_cvv = forms.CharField(widget=forms.PasswordInput,
                               validators=[RegexValidator(regex='^.{3}$', message='Please Enter a Valid CVV')])
    expiry_date = forms.DateField(widget=DateInput(attrs={'id': 'example-month-input'}))

    class Meta:
        model = CreditCard
        fields = ('card_no', 'card_cvv', 'expiry_date')

    def clean(self):
        cleaned_data = super().clean()
        expiry_date = cleaned_data.get("expiry_date")

        if (expiry_date < datetime.date.today()):
            raise forms.ValidationError("This card has Expired")

        return cleaned_data


class UserHealthForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Register.objects.filter(role='Customer'))

    class Meta:
        model = UserHealth
        exclude = ('instructor', 'transformation_status')


class UserHealthUpdateForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Register.objects.filter(role='Customer'))

    class Meta:
        model = UserHealth
        fields = ('name', 'height', 'weight', 'health_issue', 'medicine_consumption')

    def __init__(self, *args, **kwargs):
        super(UserHealthUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.name
        else:
            return self.cleaned_data['name']


class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea, required=True)

    def clean_reply(self):
        reply = self.cleaned_data['reply']
        if reply == '':
            raise forms.ValidationError('This Field is required')
        return reply


class BmiCalculation(forms.Form):
    height = forms.FloatField(label='Height in cm')
    weight = forms.FloatField(label='weight in kg')
