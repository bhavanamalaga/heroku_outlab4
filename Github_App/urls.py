from django.contrib import admin
from django.http import request
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html'),name='login'),
    path('signup/', views.register, name='signup'),
    path('explore/',views.explore,name='explore'),
    path('profile/',views.profile,name='profile'),
    path('profile/<int:user_id>',views.profil,name='profil'),
    path('update_profile/<int:user_id>',views.update_profile,name='update_profile'),
    path('logout/',views.logout_request,name='logout'),
]