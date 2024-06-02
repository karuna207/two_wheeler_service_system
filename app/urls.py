from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [  
    path('',views.home,name='home'), 
    path('receptionistlogin',views.receptionistlogin,name='rlogin'), 
    path('mechaniclogin',views.mechaniclogin,name='mlogin'), 
    path('mechaniclogin/update',views.update_jobcard,name='updating_job'),
    # path('mechaniclogin/<str:username>',views.mech_dashboard,name='mechdashboard'),   
    path('receptionistlogin/receptionist_dashboard',views.recep_dashboard,name='recepdashboard'), 
    path('receptionistlogin/receptionist_dashboard/jobcard',views.createjobcard,name='createjobcard'), 
    path('receptionistlogin/receptionist_dashboard/addmechanic',views.addMechanic,name='addmechanic') 

    # path('',views.home,name="home"),
    # path('patient',views.patient,name="patient"),
    # path('doctor',views.doctor,name="doctor"),

    # path('receptionist',views.receptionist,name="receptionist"),
    # path('patient/patienthome',views.patienthome,name="patienthome"),
    # path('patient/patienthome/patientform',views.makeappointment,name="appointmentform"),
    # path('receptionist/recephome',views.recephome,name='recephome'),
    # path('receptionist/recephome/addpatient',views.addpatienttoqueue, name = 'addpatientqueue'),
    # # path('receptionist/recephome/dequeue',views.dequeue,name='dequeue'),
    # # path('receptionist/recephome/payment',views.payment,name='payment'),
    # path('receptionist/recephome/showqueuecsp',views.showqueuecsp,name='showqueue'),
    # # path('receptionist/recephome/showqueuegendoc',views.showqueuegendoc,name='queuedoc')
    # path('receptionist/recephome/showqueuegendoc',views.showqueuegendoc),
    # path('receptionist/recephome/dequeuegendoc',views.dequeuegendoc,name='dequeuegendoc'),
    # path('receptionist/recephome/dequeuecsp',views.dequeuecsp,name='dequeuecsp'),
    # path('doctor/doctorcsphome',views.doccsphome,name='doctorcsphome'),
    # path('doctor/doctorgendochome',views.gendochome,name='doctorgendochome'),
    # path("doctor/doctorcsphome/patienthis",views.patientcsphistory,name='csphistory'),
    # path("doctor/doctorcsphome/prescriptioncsp",views.presriptioncsp,name='prescription'),
    # path('doctor/doctorcsphome/showcspqueue',views.showcspqueuetodoc), 
    # path('doctor/doctorgendochome/patienthis',views.patientgendochistory),
    # path('doctor/doctorgendochome/showgendocqueue',views.showgendocqueue),
    # path('doctor/doctorgendochome/prescriptiongendoc',views.presriptiongendoc),
    # path('receptionist/recephome/emergency',views.emergency),
    # path('receptionist/recephome/clearappointments',views.clearappointments)
    # path('receptionist/recephome/makepayment',views.makepayment,name='payment')
    # path('doctor/doctorhome/patienthis',views.patienthistory,name='patienthis')

]