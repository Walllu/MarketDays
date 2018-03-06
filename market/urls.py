from django.conf.urls import url
from market import views
from django.conf import settings
from django.conf.urls.static import static
# NOTE: This urls.py file was not generated, I had to make it -- Walter 27.2.2018
urlpatterns = [
    #assuming we want to name the initial portal to the app "index"
    #url(r'^$', views.index, name='index'),
    url(r'^users/', views.users, name = 'users'),
    url(r'^userProfile/', views.userProfile, name = 'userProfile'),
    url(r'^$', views.index, name='index'),
    url(r'^restricted/', views.restricted, name='restricted'),

    ]
