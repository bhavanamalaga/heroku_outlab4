from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)
    last_updated = models.CharField(max_length=300)
    models.DateField

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class repo(models.Model):
    Profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    stars = models.IntegerField()
    name = models.CharField(max_length=200)
    