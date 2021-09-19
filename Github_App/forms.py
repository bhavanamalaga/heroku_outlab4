from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
import requests
from .request import convert_time,time


class UserRegisterForm(UserCreationForm):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100,required=False)

    class Meta:
        model = User
        fields = ['username', 'password1','password2','firstname','lastname']

    def save(self, commit=True):
            user = super(UserRegisterForm, self).save(commit=False)
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['firstname']
            user.last_name = self.cleaned_data['lastname']
            
            if commit:
                user.save()
            
            r = requests.get('https://api.github.com/users/'+user.username).json()
            time = convert_time()
            Profile.objects.create(user = user,followers= r['followers'], last_updated= time,)

            profil = Profile.objects.get(user = user)
            r1 = requests.get('https://api.github.com/users/'+user.username+'/repos').json()
            
            r3={}

            for i in r1:
                r3[i['name']]= i['stargazers_count']
            a= sorted(r3.items(), key=lambda x: x[1], reverse=True)
            for i,j in a:
                repo.objects.create(Profile = profil,stars = j,name=  i)
            
            return user