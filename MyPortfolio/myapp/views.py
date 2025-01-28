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
from myapp.utils import format_headers
#To fetch and store the IP and location of the user
import pandas as pd
# import geoip2.database
from django.http import JsonResponse
import psycopg2  # Example for PostgreSQL, adapt according to your database

# Get the environment variables
# DATABASE_URL = os.getenv('DATABASE_URL')


# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = #os.getenv('DB_PASSWORD')
# DB_NAME =os.getenv('DB_NAME')
# DB_HOST= os.getenv('DB_HOST')

# # Connect to the database
# db = psycopg2.connect(
#     dbname=DATABASE_URL,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host= DB_HOST,  # Add other parameters as needed
#     # port=os.getenv('DB_PORT')
# )



# db= psycopg2.connect(DATABASE_URL)



# Create your views here.
# MySQL DB Configuration

# Establish a database connection 
db = MySQLdb.connect( host="localhost",user='root', 
                      passwd='root', db=  'flask_users' )

#For postgres




cursor =db.cursor()

# def home(request):
#     return render(request, "home.html")


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# def store_user_connection(request):
    # try:
    #     filename = f"user_log_{dt.datetime.now().strftime('%Y-%m-%d')}.csv"
    #     ip_address = get_client_ip(request)
    #     # Get the absolute path of the file 
    #     geo_file_path = os.path.abspath('myapp/GeoLite2-City.mmdb')
    #     reader = geoip2.database.Reader(geo_file_path)
    #     response = reader.city(ip_address)

    #     # Create a dictionary with the user data
    #     user_data = {
    #         'ip_address': [ip_address],
    #         'city': [response.city.name],
    #         'country': [response.country.name],
    #         'latitude': [response.location.latitude],
    #         'longitude': [response.location.longitude],
    #         'timestamp': [pd.Timestamp.now()],
        
    #     }

    #     # Convert the dictionary to a DataFrame
    #     df = pd.DataFrame(user_data)

    #     # Append the DataFrame to the CSV file
    #     csv_file_path = filename#'path/to/user_connections.csv'
    #     try:
    #         df.to_csv(csv_file_path, mode='a', header=False, index=False)
    #     except FileNotFoundError:
    #         df.to_csv(csv_file_path, mode='w', index=False)

    #     return True,csv_file_path    #JsonResponse({'status': 'success'})
    # except Exception as e:
    #     print("Exception while fetching the geolocation data",e)
    #     return False,""


def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        print("INSIDE POST METHOD OF VIEWS")
        name = request.POST.get("name")
        email = request.POST.get("email")
        country_code = request.POST.get("countrycode")
        phone  = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        print("Message Inputs : ",name,email,phone,subject,message)
        subject= format_headers(subject,remove_punc=True)
        name= format_headers(name,remove_punc=True)
        if len(name)>1 and len(name)<=50 :
            pass
        else:
            messages.error(request,"Length of the name should be greater than 2 and less than 30 characters ")
            return render(request,'home.html') 
        if "@" not in email or "." not in email:  #or ".com" not in email
            messages.error(request,"Invalid email address!")
            return render(request,'home.html') 
        if  not re.fullmatch(r"[+]\d{2}", country_code):
            messages.error(request,"Invalid country code.\n Please provide your country code . E.g. +49,+91")
          
            return render(request,'home.html')
        if not re.fullmatch(r"\d{10}", phone):
        # if len(phone)!=13 or "+" not in phone:
            messages.error(request,"Invalid Phone number.\n Please provide your 10 digit mobile number. E.g. +49,+91")
          
            return render(request,'home.html')
        if len(format_headers(subject, remove_punc= True))<5:
            messages.error(request, "Invalid subject matter.Please provide a short descriptive reason to request an appointment!")
            return render(request,'home.html')

        ins = Contact(name=name, mobile = country_code+phone, email=email,subject= subject, content = message)
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
        response = JsonResponse({'success': True, 'message': 'Form submitted successfully!'})
        response['Access-Control-Allow-Origin'] = '*'
        response["content-type"]= "application/json"
        print("The response being sent",response)
        return response
        # messages.success(request, "Your appointment has been successfully requested!")
        # return render(request,'home.html')

        
    print("INSIDE GET METHOD OF VIEWS", request)
#     get_ip_address, filepath = store_user_connection(request)
#    # Get the current time 
#     now = dt.datetime.now().time() # Define the start and end times 
#     start_time = dt.time(8, 0) # 21:00 
#     end_time = dt.time(23, 58) # 23:58 # Check if the current time is within the range 
#     if start_time <= now <= end_time and get_ip_address:
#         query= """SELECT * FROM email_notification_creds ORDER BY id DESC LIMIT 1;"""
#         cursor.execute(query)
#         row= cursor.fetchone()
#         column_names = [description[0] for description in cursor.description]
#         cred_dict = dict(zip(column_names, row))
#         cred_dict['reciever']= "mr.prakhar@gmail.com"
#         # cred_dict['inviting_person']= name
#         cred_dict['notification_type']= "daily_visit_log"
#         cred_dict['attachment_filepath']= filepath
        
#         cred_dict['custom_message']= """Please find the daily visit log attached to this email."""
#         cred_dict['signature'] = """\nRegards,\n Prakhar's Email BOT"""
#         cred_dict['subject'] = f"Daily log emailed and deleted at  : {dt.datetime.now()}"
#         cred_dict['signature'] = """\nRegards,\n Prakhar's Email BOT"""
#         send_notification= send_mail(cred_dict,automation_type="log")
        # print("Daily log sent")

    return render(request,'home.html') 