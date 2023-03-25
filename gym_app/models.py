from django.contrib.auth.models import AbstractUser
from django.db import models


class Batch(models.Model):
    batch_name = models.CharField(max_length=50)
    batch_time = models.TimeField()

    def __str__(self):
        return self.batch_name


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_physician = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)


class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='register')
    role = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=50)
    phone_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    address = models.TextField(max_length=100)
    qualification = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profile')
    consultation_time = models.TimeField(null=True, blank=True)
    required_batch_name = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='Batch.batch_name+',
                                            null=True, blank=True)
    required_batch_time = models.CharField(max_length=200,null=True, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,related_name='batch')
    instructor = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='instructor')


class Bill(models.Model):
    name = models.ForeignKey(Register, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    present_days = models.IntegerField()
    bill_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    due_date = models.DateField()
    paid_on = models.DateField(auto_now=True)
    status = models.IntegerField(default=0)



class Services(models.Model):
    service = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='service')


class Equipment(models.Model):
    equipment = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='equipment')


class UserHealth(models.Model):
    name = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='Register.name+')
    instructor = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    height = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    health_issue = models.CharField(max_length=50)
    medicine_consumption = models.TextField()
    transformation_status = models.CharField(max_length=50, null=True)


class DietPlan(models.Model):
    heading = models.CharField(max_length=50)
    plan = models.ImageField()


class Attendance(models.Model):
    name = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='attendance')
    attendance = models.CharField(max_length=10)
    date = models.DateField()


class FirstAid(models.Model):
    cause = models.CharField(max_length=50)
    first_aid1 = models.CharField(max_length=50)
    first_aid2 = models.CharField(max_length=50, blank=True, null=True)
    first_aid3 = models.CharField(max_length=50, blank=True, null=True)
    first_aid4 = models.CharField(max_length=50, blank=True, null=True)


class Appointment(models.Model):
    user_name = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='Register.name+')
    physician = models.ForeignKey(Register, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)


class Doubts(models.Model):
    user_name = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='Register.name+')
    physician = models.ForeignKey(Register, on_delete=models.CASCADE)
    doubts = models.TextField(max_length=200)
    reply = models.TextField(max_length=200, null=True, blank=True)


class Complaints(models.Model):
    user_name = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)
    complaint = models.TextField(max_length=100)
    reply = models.TextField(max_length=100, null=True, )


class CreditCard(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=30)
    card_cvv = models.CharField(max_length=30)
    expiry_date = models.CharField(max_length=200)
