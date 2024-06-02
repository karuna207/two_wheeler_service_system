
import pickle as p
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect 
from django.db import connection 
import csv
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib import messages


class JobCard:
    def __init__(self, vehicle_reg_number, owner_details, engine_number, service_type, expected_delivery_date, assigned_mechanic=None):
        # mech=[]

        
            
        self.vehicle_reg_number = vehicle_reg_number
        self.owner_details = owner_details
        self.engine_number = engine_number
        self.service_type = service_type
        self.expected_delivery_date = expected_delivery_date
        self.completed = False
        self.additional_info = {}   
        mech_path=r'D:\twowheeler\twowheeler\data\mech.pickle' 
        job_path=r'D:\twowheeler\twowheeler\data\job.pickle'
        with open(mech_path,'rb') as f:
            entire_data=p.load(f) 

        assigned_mechanic=JobCardFactory.mechanic_least_workload(entire_data)  
        print(assigned_mechanic)
        self.assigned_mechanic=assigned_mechanic  
        # entire_data[assigned_mechanic].assign_job(self)  

            
        
        with open(job_path,'rb') as f: 
            try:
                data=p.load(f)   
                if self.owner_details in data: 
                    if  data[self.owner_details].vehicle_reg_number== self.vehicle_reg_number and data[self.owner_details].completed==False: 
                        print('job card already created and in pending state') 
                    else:
                        data[self.owner_details]=self  
                        print('data overridden') 
                        with open(mech_path,'wb') as f: 
                            entire_data[assigned_mechanic].assign_job(self)
                            p.dump(entire_data,f)
                else:
                    data[self.owner_details]=self  
                    print('new data added') 
                    with open(mech_path,'wb') as f: 
                            entire_data[assigned_mechanic].assign_job(self)
                            p.dump(entire_data,f)
            except:
                data=dict()  
                data[self.owner_details]=self  
                with open(mech_path,'wb') as f: 
                        entire_data[assigned_mechanic].assign_job(self)
                        p.dump(entire_data,f)

        with open(job_path,'wb') as f:
            p.dump(data,f)  

                




        


#         import csv

# # Load mechanic data from CSV
#         mech_file = 'data\mech.csv'
#         with open(mech_file, 'r', newline='') as csvfile:
#             mech_reader = csv.reader(csvfile) 
#             print(mech_reader) 
#             # for i in mech_reader:
#             #     print(i) 
#             #     print(1)
#             mech = list(mech_reader)
#             print(mech)
#         # Call the function to assign mechanic to a job
#         assigned_mechanic = JobCardFactory.mechanic_least_workload(mech) 
#         print(assigned_mechanic)
#         assigned_mechanic.assign_job(self)
#         self.assigned_mechanic = assigned_mechanic  # Mechanic assigned to the job

#         # Update the mechanic's workload in the CSV
#         for idx, mechanic in enumerate(mech):
#             if mechanic[0] == assigned_mechanic.username:  # Assuming 'username' is the first column in the CSV
#                 mech[idx] = [assigned_mechanic.username,p.dumps(assigned_mechanic)]
#                 break

#         # Save the updated mechanics list back to the CSV file
#         with open(mech_file, 'w', newline='') as csvfile:
#             mech_writer = csv.writer(csvfile)
#             mech_writer.writerows(mech)

#         # Append the created job card to a job card CSV file
#         jobcard_file = 'data\jobcard.csv'
#         with open(jobcard_file, 'a', newline='') as csvfile:
#             jobcard_writer = csv.writer(csvfile)
#             jobcard_writer.writerow([self.owner_details,self.vehicle_reg_number,p.dumps(self)])  # Replace attributes with actual data

#         # If self is an object that contains attributes, update the above line with the corresponding attributes

#         # Assuming self.attribute1, self.attribute2, ... correspond to the columns in the job card CSV file




    def update_additional_info(self, info):
        """
        Update additional information in the job card based on the service type.
        """
        self.additional_info.update(info)

    def assign_mechanic(self, mechanic):
        """
        Assign a mechanic to the job.
        """
        self.assigned_mechanic = mechanic

    def mark_as_completed(self):
        """
        Mark the job card as completed after the service is done.
        """
        self.completed = True

    def get_job_card_details(self):
        """
        Get job card details.
        """
        details = {
            "Vehicle Registration Number": self.vehicle_reg_number,
            "Owner Details": self.owner_details,
            "Engine Number": self.engine_number,
            "Service Type": self.service_type,
            "Expected Delivery Date": self.expected_delivery_date,
            "Completed": self.completed,
            "Assigned Mechanic": self.assigned_mechanic,
            "Additional Information": self.additional_info
        }
        return details


class MaintenanceJobCard(JobCard):
    def __init__(self, vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic=None):
        super().__init__(vehicle_reg_number, owner_details, engine_number, 'Maintenance', expected_delivery_date, assigned_mechanic)


class OilServiceJobCard(JobCard):
    def __init__(self, vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic=None):
        super().__init__(vehicle_reg_number, owner_details, engine_number, 'Oil Service', expected_delivery_date, assigned_mechanic)

class BrakeConditionJobCard(JobCard):
    def __init__(self, vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic=None):
        super().__init__(vehicle_reg_number, owner_details, engine_number, 'Brake Condition', expected_delivery_date, assigned_mechanic)


class JobCardFactory:
    @staticmethod
    def create_job_card(service_type, vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic=None):
        """
        Factory method to create different types of job cards based on the service type.
        """ 
        # mech=[]

        # f=open('mechanic.pickle','rb')  
        # while True:
        #     try:
        #         data=p.load(f) 
        #         mech.append(data) 
        #     except:
        #         break 
        # assigned_mechanic=JobCardFactory.mechanic_least_workload() 
        # assigned_mechanic.assign_job(self)
            

        if service_type.lower() == 'maintenance':
            return MaintenanceJobCard(vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic)
        elif service_type.lower() == 'oil service':
            return OilServiceJobCard(vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic)
        elif service_type.lower() == 'brake condition':
            return BrakeConditionJobCard(vehicle_reg_number, owner_details, engine_number, expected_delivery_date, assigned_mechanic)
        else:
            raise ValueError("Invalid service type specified")   
        
    @staticmethod 
    def mechanic_least_workload(mechanics_dict):
        if not mechanics_dict:
            return None

        min_workload_username = None
        min_pending_jobs = float('inf')  # Set initial pending jobs to infinity

        for username, mechanic_object in mechanics_dict.items():
            # Assuming the mechanic object has a 'jobs_pending' attribute
            if len(mechanic_object.jobs_pending) < min_pending_jobs:
                min_pending_jobs = len(mechanic_object.jobs_pending)
                min_workload_username = username

        return min_workload_username

        
    # @staticmethod 
    # def mechanic_least_workload(mechanics):
    #     if not mechanics:
    #         return None
    #     print(mechanics[0][1])
    #     min_workload_mechanic = p.loads(mechanics[0][1].encode('utf-8'))  # Initialize with the first mechanic
    #     min_pending_jobs = len(min_workload_mechanic.jobs_pending)

    #     for mechanicrow in mechanics[1:]:
    #         if len(p.loads(mechanicrow[1].encode('utf-8')).jobs_pending) < min_pending_jobs:
    #             min_pending_jobs = len(p.loads(mechanicrow[1].encode('utf-8')).jobs_pending)
    #             min_workload_mechanic = p.dumps(mechanicrow[1].encode('utf-8'))

    #     return min_workload_mechanic
        



# Example usage:
# maintenance_job_card = MaintenanceJobCard('ABC123', 'John Doe', '12345', '2023-12-20', 'Mechanic1')
# oil_service_job_card = OilServiceJobCard('DEF456', 'Jane Smith', '67890', '2023-12-22', 'Mechanic2')

# maintenance_job_card.assign_mechanic('Mechanic1')
# oil_service_job_card.assign_mechanic('Mechanic2')

# print(maintenance_job_card.get_job_card_details())
# print(oil_service_job_card.get_job_card_details())



# from django.contrib.auth.models import User
# from django.contrib.auth import logout, authenticate, login
# import csv
# from abc import ABC, abstractmethod
# from datetime import datetime



#mechanic 


class Mechanic:
    
    def __init__(self, name,username,password,contact):
        self.name = name 
        self.username=username 
        self.password=password
        self.contact = contact
        self.jobs_pending = [] 
        
        
        import csv

# Data to be checked
        data_to_check = [self.username, self.password, False, True, 'e']

# File paths
        # mech_csv_path = r"D:\twowheeler\twowheeler\data\mech.csv"
        login_details_csv_path = r'D:\twowheeler\twowheeler\data\login_details.csv' 
        mech_path=r'D:\twowheeler\twowheeler\data\mech.pickle'

        
        
        def check_data_in_logincsv(file_path, data):
            with open(file_path, 'r', newline='') as csvfile: 
                try:
                    reader = csv.reader(csvfile)  
                    for row in reader:
                    # Check if the entire row matche the data to be checked
                        if row[0] == data[0]:
                            return True  # Data already exists
                    return False  # Data not found in the file
        # Check if data exists in mech.csv
        
                except:
                    print('login csv doesnt contain any details') 
                    with open(file_path,'a',newline='') as f:
                        writer=csv.writer(f)  
                        print(data)
                        writer.writerow(data)
              
        

        
        # Check if data exists in login_details.csv
        
        data_exists_in_login_details = check_data_in_logincsv(login_details_csv_path, data_to_check)
        
        if not data_exists_in_login_details:
            with open(login_details_csv_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data_to_check)
            print("Data appended to login_details.csv")
        else:
            print("Data already exists in login_details.csv")   

        with open(mech_path,'rb') as f: 
            try:
                entire_data= p.load(f) #entire_data is in dictionary format  
                if entire_data:
                    if self.username not in  entire_data: 
                        entire_data[self.username]=self 
                    else:
                        print('Data already exist in mech.pickle')   
            except:
                entire_data=dict() 
                entire_data[self.username]=self

            
        with open(mech_path,'wb') as f:
            p.dump(entire_data,f) 
        
 

    def update_jobcard(self,jobcard:JobCard):
        jobcard.mark_as_completed()
        try :
            with open(r'D:\twowheeler\twowheeler\data\mech.pickle','rb')as f:
                entire_data=p.load(f)
                currentmech_obj=entire_data[self.username]
                for i in currentmech_obj.jobs_pending:
                    if i==jobcard:
                        i.mark_as_completed()

            with open(r'D:\twowheeler\twowheeler\data\mech.pickle','wb')as f:
                entire_data[currentmech_obj.username]=currentmech_obj
                p.dump(entire_data,f)
        except:
            print("error...")
        

       

        



    def assign_job(self, job_card):
        """
        Assign a job to the mechanic.
        """
        self.jobs_pending.append(job_card)

    def complete_job(self, job_card):
        """
        Mark a job as completed by the mechanic.
        """
        if job_card in self.jobs_pending:
            job_card.mark_as_completed()
            self.jobs_pending.remove(job_card)
            print(f"Job marked as completed by {self.name}")
        else:
            print("Job not found in the pending list.")

    def get_pending_jobs(self):
        """
        Get the list of pending jobs assigned to the mechanic.
        """
        return [job_card.get_job_card_details() for job_card in self.jobs_pending]

    def check_order_of_importance(self):
        """
        Check the order of importance of job cards based on expiry date.
        """
        sorted_jobs = sorted(self.jobs_pending, key=lambda x: x.expected_delivery_date)
        return [job_card.get_job_card_details() for job_card in sorted_jobs]


# Example usage (continued from previous example):
# Assuming job cards are already created (e.g., maintenance_job_card, oil_service_job_card, brake_condition_job_card)

# mechanic1 = Mechanic('John', '123-456-7890')
# mechanic1.assign_job(maintenance_job_card)
# mechanic1.assign_job(oil_service_job_card)
# mechanic1.assign_job(brake_condition_job_card)

# # Get pending jobs sorted by expiry date for Mechanic 1
# print("Mechanic 1 pending jobs sorted by expiry date:")
# print(mechanic1.check_order_of_importance())




def home(request):
    return render(request,'home.html') 

# def receptionistlogin(request):
#     return render(request,'receptionistlogin.html')
 
# def mechaniclogin(request):
#     return render(request,'mechaniclogin.html')

import csv
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def read_user_credentials(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row) 

    print(users)
    return users

def receptionistlogin(request):
    user_credentials = read_user_credentials('data\login_details.csv')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        for user in user_credentials:
            if user['username'] == username and user['password'] == password and user['is_receptionist'] == 'True':
                return redirect('receptionistlogin/receptionist_dashboard')
                # user_obj = authenticate(request, username=username, password=password)
                # if user_obj is not None:
                #     if user_obj.is_active:
                #         login(request, user_obj)
                #         return HttpResponseRedirect(reverse('receptionist_dashboard'))  # Redirect to receptionist dashboard
               
        return render(request, 'receptionistlogin.html', {'error_message': 'Invalid credentials'})
    
    return render(request, 'receptionistlogin.html')

def mechaniclogin(request):
    # user_credentials = read_user_credentials('data\login_details.csv')
    
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password') 
    #     print('hi') 
    #     print(username) 
    #     print(password)
        
    #     for user in user_credentials:
    #         if user['username'] == username and user['password'] == password and user['is_mechanic'] == 'True':
    #             # request.session['username'] = username 
    #             print('hui')
    #             return redirect('mechaniclogin/mechanic_dashboard')  
    #         else: 
    #             print('devon')
    #             pass 
    #     print('snake')
    #     return render(request,'mechaniclogin.html',{'error_message': 'Invalid credentials'})
    
    # return render(request, 'mechaniclogin.html') 
    user_credentials = read_user_credentials('data\login_details.csv')
    print('snake')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        print('hu')
        print(username) 
        print(password)
        for user in user_credentials: 
            print(user['username'])
            print(user['password']) 
            print(user['is_mechanic'])
            if user['username'] == username and user['password'] == password and user['is_mechanic'] == 'True':  
                print('dvd')
                # return redirect('mechaniclogin/<str:username>')   
                with open(r"D:\twowheeler\twowheeler\data\mech.pickle","rb") as f:
                    mech_data = p.load(f)
                    jobs_pending=mech_data[username].jobs_pending 

                sorted_jobs = sorted(jobs_pending, key=lambda x: x.expected_delivery_date)
                    
                return render(request,'profile.html',{'username':username,'job_cards':sorted_jobs})
            # 'student/shome/viewcourse/<str:username>'
                
        else:       
            return render(request, 'mechaniclogin.html')
    
    return render(request, 'mechaniclogin.html')

# import csv
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         with open('path/to/user_credentials.csv', 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if row['username'] == username and row['password'] == password:
#                     if row['is_active'] == 'True':
#                         # Successfully authenticated
#                         # You may set the user in session or perform further actions
#                         # For example:
#                         request.session['username'] = username
#                         return redirect('dashboard')  # Redirect to dashboard upon successful login

#         # If authentication fails, display an error message
#         messages.error(request, 'Invalid username or password.')
    
#     return render(request, 'login.html')



# def mech_dashboard(request,username):  
#     # return HttpResponse('this is mech dashboard') 
#     return render(request, 'profile.html', {'username': username})
 
def recep_dashboard(request):
    return render(request,'recephome.html') 

def createjobcard(request): 
    if request.method =='POST': 
        service_type= request.POST.get('service_type')
        vehicle_reg_number = request.POST.get('vehicle_reg_number')
        owner_details = request.POST.get('owner_details')
        engine_number = request.POST.get('engine_number')
        expected_delivery_date = request.POST.get('expected_delivery_date') 
        jc=JobCardFactory.create_job_card(service_type,vehicle_reg_number,owner_details,engine_number,expected_delivery_date)  
        messages.success(request,'Job Card created successfully')
    return render(request, 'create_job_card.html')
        





def addMechanic(request):
    if request.method=='POST': 
        name= request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = request.POST.get('contact') 
        m=Mechanic(name,username,password,contact)   
        if m:
            # Mechanic was successfully added, trigger an alert
            messages.success(request, 'Mechanic has been successfully created!')
        else:
            # Mechanic creation failed
            messages.error(request, 'Failed to create mechanic!')
    return render(request,'addmechanic.html') 

import json
def update_jobcard(request):
    if request.method=='POST':  
        mech_path=r'D:\twowheeler\twowheeler\data\mech.pickle' 
        job_path=r'D:\twowheeler\twowheeler\data\job.pickle'
        job_card_owner=request.POST.get('job_card') 
        print(job_card_owner)  
        with open(job_path,'rb') as f:
            data=p.load(f) 
            for i in data:
                if data[i].owner_details ==job_card_owner:
                    data[i].completed=True 
            
        with open(job_path,'wb') as f:
            p.dump(data,f)  

        with open(mech_path,'rb') as f:
            data=p.load(f) 
            newdata=dict()
            
            for i in data:
                jc_details=data[i].jobs_pending 
                new_jc_details=[]
                for jc in jc_details:
                    if jc.owner_details==job_card_owner:
                        # jc_details.remove(jc)
                        pass 
                    else:
                        new_jc_details.append(jc) 
                data[i].jobs_pending=new_jc_details 
        with open(mech_path,'wb') as f:
            p.dump(data,f)



        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        # Email configuration
        email_sender = 'twowheelerserviceproject01@gmail.com'  # Sender's email address
        email_receiver = job_card_owner  # Receiver's email address
        email_subject = 'update regarding vehicle'
        # email_body = f'Hello {job_card_owner}! .We are delighted to inform that you can now collect your vehicle from our service provider'
        email_body=f'''Dear {job_card_owner},

I hope this message finds you well.

We are pleased to inform you that your vehicle is now ready for collection from our esteemed service provider. Your vehicle has undergone the necessary maintenance and is now prepared for your use.

Please proceed to collect your vehicle. Our team has ensured that all services requested have been diligently completed to ensure the optimal functioning of your vehicle.

Should you have any queries or require further assistance, please do not hesitate to contact us.

Thank you for choosing our services. We look forward to continuing to serve you with the utmost care and dedication.'''
        # Create a multipart message and set the headers
        message = MIMEMultipart()
        message['From'] = email_sender
        message['To'] = email_receiver
        message['Subject'] = email_subject

        # Add body to email
        message.attach(MIMEText(email_body, 'plain'))

        # SMTP Server configuration
        smtp_server = 'smtp.gmail.com'  # SMTP server (e.g., smtp.gmail.com for Gmail)
        smtp_port = 587  # SMTP port number

        # Login credentials for the SMTP server
        username = 'twowheelerserviceproject01@gmail.com'
        password = 'gcukkiyllilgfgko'

        try:
            # Create a SMTP session
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(username, password)  # Login using your credentials

            # Send email
            server.sendmail(email_sender, email_receiver, message.as_string())

            print("Email sent successfully!") 
            return render(request,'Success.html') 

        except Exception as e:
            print(f"Error: {e}")  
            print('failure')
            return render(request,'Failure.html')

        # finally:
            # Quit the SMTP server session
            # server.quit()

        # return HttpResponse(job_card_owner)
        

# f=open(r'D:\twowheeler\twowheeler\data\mechanic.bin','rb')  
# data=p.load(f) 
# print(data) 
# f.close()

 


# f=open(r'D:\twowheeler\twowheeler\data\mechanic.bin','wb')   
# p.dump([],f) 
# f.close()




# addMechanic() 
# addMechanic() 
# addMechanic()








# def complete_job(self, job_card):
#         """
#         Mark a job as completed by the mechanic.
#         """
#         if job_card in self.jobs_pending:
#             job_card.mark_as_completed()
#             self.send_completion_email(job_card)
#             self.jobs_pending.remove(job_card)
#             print(f"Job marked as completed by {self.name}")
#         else:
#             print("Job not found in the pending list.")
    
#     def send_completion_email(self, job_card):
#         receiver_email = job_card.owner_details
#         subject = 'Job Completion Notification'
#         message = f"""Dear Customer,\n
#         This is to inform you that the job for vehicle registration number {job_card.vehicle_reg_number} has been completed successfully.\n
#         Thank you,
#         Mechanic {self.name} """
#         sender_email = 'sample_email@gmail.com'
#         send_mail(subject, message, sender_email, [receiver_email])
    
#     def send_email(subject, message, sender_email, receiver_email):
#         try:
#             send_mail(subject, message, sender_email, [receiver_email])
#             logger.info(f"Email sent successfully to {receiver_email}")
#         except Exception as e:
#             logger.error(f"Failed to send email to {receiver_email}. Error: {e}")