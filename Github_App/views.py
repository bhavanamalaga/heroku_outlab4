from django.core.checks import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import Profile,repo
import requests
from django.urls import reverse
from .request import convert_time,time

# Create your views here.

def home(request):
    return render(request, 'Home.html')

def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            r = requests.get('https://api.github.com/users/'+username)
            if(r.status_code == 200):
                form.save()                
                return redirect('home')
            else:
                form = UserRegisterForm()
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})

def explore(request):
    if(request.user.is_authenticated):
        name = request.user
        user1 = User.objects.get(username = name)
        all_users = User.objects.all()
        links = {}
        for i in all_users:
            if(i.username != name):
                links[i.username] = "/profile/?username="+i.username
        print(links)
        args = {'user1':user1,'links': links}
        return render(request,'explore.html',args)
    else:
        return redirect('login')

def profile(request):
    if(request.user.is_authenticated):
        user1 = User.objects.get(username = request.user)
        user = User.objects.get(username = request.GET['username'])
        profil = Profile.objects.get(user = user)
        rep = repo.objects.filter(Profile = profil)
        dict = {}
        for re in rep :
            dict[re.name] = re.stars

        args = {'user1':user1,'user':user,'dict': dict, 'profile': profil}
        print(request.user,request.GET['username'])
        if (str(request.user) == str(request.GET['username'])) :
            print("hai")
            return render(request,'profile.html',args)
        else:
            return render(request,"profile2.html",args)
    else:
        return redirect('login')

def profil(request,user_id):
    if(request.user.is_authenticated):
        user = User.objects.get(id = user_id)
        profil = Profile.objects.get(user = user)
        rep = repo.objects.filter(Profile = profil)
        dict = {}
        for re in rep :
            dict[re.name] = re.stars

        args = {'user' : user,'dict': dict, 'profile': profil}
        return render(request,'profile.html',args)
    else:
        return redirect('login')

def update_profile(request, user_id):
    if(request.user.is_authenticated):
        user = User.objects.get(id = user_id)
        r = requests.get('https://api.github.com/users/'+user.username).json()
        profil = Profile.objects.get(user = user)
        profil.delete()
        time = convert_time()
        Profile.objects.create(user = user,followers= r['followers'], last_updated= time)
        profil = Profile.objects.get(user = user)

        r1 = requests.get('https://api.github.com/users/'+user.username+'/repos').json()
                
        r3={}

        for i in r1:
            r3[i['name']]= i['stargazers_count']

        a= sorted(r3.items(), key=lambda x: x[1], reverse=True)
        
        for i,j in a:
            repo.objects.create(Profile = profil,stars = j,name=  i)
        return redirect(reverse('profil', args=[user_id]))
    else:
        return redirect('login')

def logout_request(request):
    logout(request)
    return redirect('login')
