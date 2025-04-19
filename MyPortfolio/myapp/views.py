from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpRequest,JsonResponse
from myapp.models import Contact
from myapp import models
import re
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpRequest,JsonResponse
import os
from django.conf import settings
from pathlib import Path
import json
import MySQLdb
import datetime as dt
from myapp.utils import prepare_email_template_and_send as send_mail
import os
from myapp.utils import format_headers
#To fetch and store the IP and location of the user
import pandas as pd

from django.http import JsonResponse
import psycopg2  # Example for PostgreSQL, adapt according to your database




#****************************************************** New *****************************************************



base_dir=Path(__file__).resolve().parent
# print("current dir : ",base_dir)
IMAGE_FOLDER = os.path.join(base_dir, 'static/images')
TEXT_FOLDER = os.path.join(base_dir, 'static/text')
PDF_FOLDER = os.path.join(base_dir, 'static/pdf')

print("Static url : ",settings.STATIC_URL,IMAGE_FOLDER)
# Create your views here.
def home(request):
    return render(request , "home.html")

def get_images(request):

    images = []
    
    if os.path.exists(IMAGE_FOLDER): 

        print("Exists",os.listdir(IMAGE_FOLDER)) # Ensure folder exists
        for filename in os.listdir(IMAGE_FOLDER):
            print("CHECKING : ",filename)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')) and "slideshow1" in filename.lower():
                desc_file = os.path.splitext(filename)[0] + '.txt'
                desc_path = os.path.join(TEXT_FOLDER, desc_file)
                description = open(desc_path).read().strip() if os.path.exists(desc_path) else "No description available"
                # description =description.split("*****")
                # description = "\n".join(description)
                print("ADDING : ",f'images/{filename}')
                # with open("paths.txt","a") as file:
                #     file.write( f'\nimages/{filename}')
                appname = filename.split("_")[0]
                appname = filename.split("slideshow1")[0]

                images.append({'src': f'images/{filename}','desc': description, 'filename':appname})
                
    else:
        print("Image Folder Not Found!",IMAGE_FOLDER)
    response_object = JsonResponse(images, safe=False)
        #     print("\nResponse : ",
        # json.loads(response_object.content)
        # )
    return JsonResponse(images, safe=False)


def get_events(request):

    images = []
    
    if os.path.exists(IMAGE_FOLDER): 

        print("Exists",os.listdir(IMAGE_FOLDER)) # Ensure folder exists
        for filename in os.listdir(IMAGE_FOLDER):
            print("CHECKING : ",filename)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')) and "slideshow2" in filename.lower():
                desc_file = os.path.splitext(filename)[0] + '.txt'
                desc_path = os.path.join(TEXT_FOLDER, desc_file)
                description = open(desc_path).read().strip() if os.path.exists(desc_path) else "No description available"
                print("ADDING : ",f'images/{filename}')
                with open("paths.txt","a") as file:
                    file.write( f'\nimages/{filename}')


                images.append({'src': f'images/{filename}','desc': description.split("*****")[1],"heading":description.split("*****")[0]})
                
    else:
        print("Slide Folder Not Found!",IMAGE_FOLDER)
    response_object = JsonResponse(images, safe=False)
        #     print("\nResponse : ",
        # json.loads(response_object.content)
        # )
    return response_object


def get_locations(request):

    images = []
    
    if os.path.exists(TEXT_FOLDER): 

        # print("Exists",os.listdir(TEXT_FOLDER)) # Ensure folder exists
        for filename in os.listdir(TEXT_FOLDER):
            print("CHECKING text : ",filename)
            if filename.lower().endswith(('txt')) and "locations" in filename.lower():
                desc_file = os.path.splitext(filename)[0] + '.txt'
                desc_path = os.path.join(TEXT_FOLDER, desc_file)
                description = open(desc_path).read().strip() if os.path.exists(desc_path) else "No description available"
                print("Now ADDING : ",f'{description.split("...>>")}')
                # with open("paths.txt","a") as file:
                #     file.write( f'\nimages/{filename}')
                for loc in description.split("...>>"):
                    if len(loc.strip())==0:
                        continue

                    images.append({'src': f'text/{filename}','desc': loc})
                
    else:
        print("Slide Folder Not Found!",IMAGE_FOLDER)
    response_object = JsonResponse(images, safe=False)
        #     print("\nResponse : ",
        # json.loads(response_object.content)
        # )
    return response_object
    

def get_certificates(request):

    images = []
    
    if os.path.exists(IMAGE_FOLDER): 

        print("Exists",os.listdir(PDF_FOLDER)) # Ensure folder exists
        for filename in os.listdir(PDF_FOLDER):
            print("CHECKING : ",filename)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf')) and "slideshow_3" in filename:
                desc_file = os.path.splitext(filename)[0] + '.txt'
                desc_path = os.path.join(TEXT_FOLDER, desc_file)
                description = open(desc_path).read().strip() if os.path.exists(desc_path) else "No description available"
                print("ADDING : ",f'\npdf/{filename}')
                with open("paths.txt","a") as file:
                    file.write( f'\npdf/{filename}')


                images.append({'src':f'pdf/{filename}','desc': description, 'filename':filename.split("_")[0]})
                
    else:
        print("PDF Folder Not Found!",PDF_FOLDER)
    response_object = JsonResponse(images, safe=False)
        #     print("\nResponse : ",
        # json.loads(response_object.content)
        # )
    return JsonResponse(images, safe=False)



def get_skillset(request):

    images = []
    
    if os.path.exists(TEXT_FOLDER): 

        # print("Exists",os.listdir(TEXT_FOLDER)) # Ensure folder exists
        for filename in os.listdir(TEXT_FOLDER):
            print("CHECKING text : ",filename)
            if filename.lower().endswith(('txt')) and "skillset" in filename.lower():
                desc_file = os.path.splitext(filename)[0] + '.txt'
                desc_path = os.path.join(TEXT_FOLDER, desc_file)
                description = open(desc_path).read().strip() if os.path.exists(desc_path) else "No description available"
                print("Now ADDING : ",f'{description.split("...>>")}')
                # with open("paths.txt","a") as file:
                #     file.write( f'\nimages/{filename}')
                for skill in description.split(",...>>"):
                    if len(skill.strip())==0:
                        continue

                    images.append({'src': skill.split("|")[0],'desc': skill.split("|")[1]})
                
    else:
        print("Slide Folder Not Found!",IMAGE_FOLDER)
    response_object = JsonResponse(images, safe=False)
        #     print("\nResponse : ",
        # json.loads(response_object.content)
        # )
    return response_object
    