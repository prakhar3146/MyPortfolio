from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpRequest,JsonResponse
from myapp.models import Contact
from myapp import models
import re
import MySQLdb
import datetime as dt
from myapp.utils import prepare_email_template_and_send as send_mail
import os
import psycopg2  # Example for PostgreSQL, adapt according to your database

# Get the environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Connect to the database
db = psycopg2.connect(
    dbname=DATABASE_URL,
    user=DB_USER,
    password=DB_PASSWORD,
    host=os.getenv('DB_HOST'),  # Add other parameters as needed
    port=os.getenv('DB_PORT')
)





# # Example function to interact with the database
# def get_data():
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM your_table_name")
#     data = cursor.fetchall()
#     cursor.close()
#     return data




# Create your views here.
# MySQL DB Configuration

# Establish a database connection 
# db = MySQLdb.connect( host="localhost",user='root', 
#                       passwd='root', db=  'flask_users' )

#For postgres




cursor =db.cursor()

# def home(request):
#     return render(request, "home.html")

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        print("INSIDE POST METHOD OF VIEWS")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone  = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        print("Message Inputs : ",name,email,phone,subject,message)
        
        if len(name)>1 and len(name)<=50:
            pass
        else:
            messages.error(request,"Length of the name should be greater than 2 and less than 30 characters ")
            return render(request,'home.html') 
        if "@" not in email or ".com" not in email:
            messages.error(request,"Invalid email address!")
            return render(request,'home.html') 
        if len(phone)!=13 or "+" not in phone:
            messages.error(request,"Invalid Phone number.\n Please provide your mobile number followed by the country code. E.g. +49,+91")
            # return render(request,'home.html') 
            return render(request,'home.html')
        if len(subject.strip())<5:
            messages.error(request, "Invalid subject matter.Please provide a short descriptive reason to request an appointment!")


        ins = Contact(name=name, mobile = phone, email=email,subject= subject, content = message)
        ins.save()
        messages.success(request, "Thanks for reaching out! \nYour message has been sent to Prakhar and he will be contacting you asap. \n Good Day! ")
        print("Data saved")
        #Notifying both the parties on contact
        query= """SELECT * FROM email_notification_creds ORDER BY id DESC LIMIT 1;"""
        cursor.execute(query)
        row= cursor.fetchone()
        column_names = [description[0] for description in cursor.description]
        cred_dict = dict(zip(column_names, row))

        cred_dict['reciever']= email
        cred_dict['inviting_person']= name
        cred_dict['notification_type']= "appointment_booking"
        cred_dict['username']= name
        cred_dict['custom_message']= """Thank you for contacting Prakhar.\n This is to notify you that the appointment request has been raised to Prakhar and you can expect to hear from him soon.\n """
        cred_dict['signature'] = """\nRegards,\n Prakhar's Email BOT"""
        cred_dict['subject'] = f"Appointment Request Generated at  : {dt.datetime.now()} regarding {subject}"
        #Sending email notification
        print("CRED DICT :  ",cred_dict)
        send_notification= send_mail(cred_dict,automation_type="portfolio")
        print("Notification 1 result : ", send_notification)
        cred_dict['custom_message']= f"""Prakhar you have an appointment request  from :\n {name} ,
         \nContact number : {phone}, \nEmail Id : {email} with message : {message}"""
        cred_dict['reciever']= """mr.prakhar@gmail.com"""
        send_notification= send_mail(cred_dict,automation_type="portfolio")
        print("Notification 2 result : ", send_notification)
        # return render(request,'home.html') 
        return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})

        
    print("INSIDE GET METHOD OF VIEWS", request)
    return render(request,'home.html') 