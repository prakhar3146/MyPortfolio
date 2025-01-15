from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=400)
    email = models.EmailField(max_length= 400)
    mobile = models.CharField(max_length= 13)
    subject= models.CharField(max_length=400)
    content = models.TextField( max_length= 400)
