from django.urls import path
from . import views


urlpatterns = [
    # path('',views.contact, name= 'homepage'),
        path("", views.home,name = 'home'),
    path('get_images/', views.get_images, name='get_images'),
    path('get_events/', views.get_events, name='get_events'),
    path('get_locations/', views.get_locations, name='get_locations'),
    path('get_certificates/', views.get_certificates, name='get_certificates/'),
    path('get_skillset/', views.get_skillset, name='get_skillset/'),
]