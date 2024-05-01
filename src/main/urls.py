from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home , name='home'),
    path('signup', views.sign_up , name='sign_up'),
    path('post_create' , views.post_create , name='post_create')
    

]