from django.contrib import admin
from django.urls import path
from gym_app import views, adminviews, instructorviews,physicianviews,userviews

urlpatterns = [

    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('index/',views.batches, name='batches'),
    path('instructor/',views.instructor, name='instructor'),
    path('contact/',views.contact, name='contact'),
    path('batches/',views.batches, name='batches'),
    path('service/',views.service, name='service'),
    path('gallery/',views.gallery, name='gallery'),
    path('login_view/',views.login_view, name='login_view'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('instructor_register/', views.instructor_register, name='instructor_register'),
    path('physician_register/', views.physician_register, name='physician_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('view_staff/', adminviews.staff_view, name='view_staff'),
    path('delete_staff/<int:id>/', adminviews.delete_staff, name='delete_staff'),
    path('logout_view/', views.logout_view, name='logout_view'),

    path('view_user/', adminviews.user_view, name='view_user'),
    path('approve_user/<str:user_id>/', adminviews.approve_user, name='approve_user'),
    path('add_batch/', adminviews.add_batch, name='add_batch'),
    path('add_instructor/', adminviews.add_instructor, name='add_instructor'),
    path('view_attendance_admin/', adminviews.view_attendance_admin, name='view_attendance_admin'),
    path('add_bill/', adminviews.bill, name='add_bill'),
    path('view_bill/', adminviews.view_bill, name='view_bill'),
    path('add_service/', adminviews.add_service, name='add_service'),
    path('view_service/', adminviews.view_service, name='view_service'),
    path('edit_service/<int:id>/', adminviews.edit_service, name='edit_service'),
    path('delete_service/<int:id>/', adminviews.delete_service, name='delete_service'),
    path('view_complaint/', adminviews.view_complaint, name='view_complaint'),
    path('reply_complaint/<int:id>/', adminviews.reply_complaint, name='reply_complaint'),
    path('delete_complaint/<int:id>/', adminviews.delete_complaint, name='delete_complaint'),
    path('add_equipment/', adminviews.add_equipment, name='add_equipment'),
    path('view_equipment/', adminviews.view_equipment, name='view_equipment'),
    path('edit_equipment/<int:id>/', adminviews.edit_equipment, name='edit_equipment'),
    path('delete_equipment/<int:id>/', adminviews.delete_equipment, name='delete_equipment'),
    path('day_attendance_admin/<date>/', adminviews.day_attendance_admin, name='day_attendance_admin'),
    path('ajax/load-batch/', views.load_batch, name='ajax_load_batch'),  # AJAX
    path('ajax/load-bill/', adminviews.load_bill, name='ajax_load_bill'),  # AJAX
    path('view_batches/', adminviews.view_batches, name='view_batches'),  # AJAX

    path('instructor_page/', views.instructor_page, name='instructor_page'),
    path('add_health/', instructorviews.add_health, name='add_health'),
    path('view_health/', instructorviews.view_health_issue, name='view_health'),
    path('edit_health/<int:id>/', instructorviews.edit_health_issue, name='edit_health_issue'),
    path('add_diet/', instructorviews.add_diet, name='add_diet'),
    path('view_diet/', instructorviews.view_diet, name='view_diet'),
    path('edit_diet/<int:id>/', instructorviews.edit_diet, name='edit_diet'),
    path('delete_diet/<int:id>/', instructorviews.delete_diet, name='delete_diet'),
    path('add_attendance/', instructorviews.add_attendance, name='add_attendance'),
    path('view_attendance/', instructorviews.view_attendance, name='view_attendance'),
    path('view_firstaid_instructor/', instructorviews.view_firstaid_instructor, name='view_firstaid_instructor'),
    path('mark/<int:id>/', instructorviews.mark, name='mark'),
    path('day_attendance/<date>/', instructorviews.day_attendance, name='day_attendance'),




    path('physician_page/', views.physician_page, name='physician_page'),
    path('view_user_health/', physicianviews.view_user_health, name='view_user_health'),
    path('edit_user_health/<int:id>/', physicianviews.edit_user_health, name='edit_user_health'),
    path('view_appointment/', physicianviews.view_appointment, name='view_appointment'),
    path('approve_appointment/<int:id>/', physicianviews.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:id>/', physicianviews.reject_appointment, name='reject_appointment'),
    path('add_first_aid/', physicianviews.add_first_aid, name='add_first_aid'),
    path('view_first_aid/', physicianviews.view_first_aid, name='view_first_aid'),
    path('edit_first_aid/<int:id>/', physicianviews.edit_first_aid, name='edit_first_aid'),
    path('delete_first_aid/<int:id>/', physicianviews.delete_first_aid, name='delete_first_aid'),
    path('view_medicaldoubts_physician/', physicianviews.view_medicaldoubts_physician, name='view_medicaldoubts_physician'),
    path('reply_doubt/<int:id>/', physicianviews.reply_doubts, name='reply_doubts'),
    path('consultation_time/', physicianviews.consultation_time, name='consultation_time'),


    path('user_page/', views.user_page, name='user_page'),
    path('view_batch_user/',userviews.view_batch_user, name='view_batch_user'),
    path('view_diet_user/',userviews.view_diet_user, name='view_diet_user'),
    path('take_appointment/',userviews.take_appointment, name='take_appointment'),
    path('view_appointment_user/',userviews.view_appointment_user, name='view_appointment_user'),
    path('view_equipment_user/', userviews.view_equipment_user, name='view_equipment_user'),
    path('ask_doubts/', userviews.ask_doubts, name='ask_doubts'),
    path('view_doubt/', userviews.view_doubt, name='view_doubt'),
    path('edit_doubt/<int:id>/', userviews.edit_doubt, name='edit_doubt'),
    path('delete_doubt/<int:id>/', userviews.delete_doubt, name='delete_doubt'),
    path('add_complaint/', userviews.add_complaint, name='add_complaint'),
    path('view_complaint_user/', userviews.view_complaint_user, name='view_complaint_user'),
    path('view_attendance_user/', userviews.view_attendance_user, name='view_attendance_user'),
    path('get_invoice/<int:id>/', userviews.get_invoice, name='get_invoice'),
    path('view_invoice/<int:id>/', userviews.view_invoice, name='view_invoice'),

    path('view_bill_user/', userviews.view_bill_user, name='view_bill_user'),
    path('pay_bill/<int:id>/', userviews.pay_bill, name='pay_bill'),
    path('bill_history/', userviews.bill_history, name='bill_history'),
    path('view_transformation/', userviews.view_transformation, name='view_transformation'),
    path('bmi/', userviews.bmi, name='bmi'),
    path('view_bmi/<bmi>/', userviews.view_bmi, name='view_bmi'),
    path('drop_gym/', userviews.drop_gym, name='drop_gym'),
    path('pay_in_direct/<int:id>/', userviews.pay_in_direct, name='pay_in_direct'),

]