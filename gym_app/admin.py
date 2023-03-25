from django.contrib import admin


from gym_app import models

admin.site.register(models.User)
admin.site.register(models.Register)
admin.site.register(models.Appointment)
admin.site.register(models.Attendance)
admin.site.register(models.FirstAid)
admin.site.register(models.Batch)
admin.site.register(models.Bill)
admin.site.register(models.Doubts)
admin.site.register(models.Services)
admin.site.register(models.Equipment)
admin.site.register(models.UserHealth)
admin.site.register(models.DietPlan)
admin.site.register(models.Complaints)
admin.site.register(models.CreditCard)
admin.site.register(models.Instructor)
