from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    movie_name=models.CharField(max_length=50)
    movie_desc=models.CharField(max_length=200)
    movie_img=models.ImageField()