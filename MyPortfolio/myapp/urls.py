from django.urls import path
from . import views


urlpatterns = [
    path('',views.contact, name= 'homepage'),
    path('about/',views.about,name="about")
]