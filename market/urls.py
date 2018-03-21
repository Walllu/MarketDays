from django.conf.urls import url
from market import views
from django.conf import settings
from django.conf.urls.static import static
# NOTE: This urls.py file was not generated, I had to make it -- Walter 27.2.2018
urlpatterns = [
    #assuming we want to name the initial portal to the app "index"
    #url(r'^$', views.index, name='index'),
    url(r'^users/', views.users, name = 'users'),
    url(r'^sessionlist/', views.sessionlist, name='sessionlist'),
    url(r'^join_session/(?P<session_slug>[\w\-]+)/$', views.join_session, name='join_session'),
    url(r'^viewuser/(?P<user_name_slug>[\w\-]+)/$', views.view_user, name='view_user'), # this is for all people to be able to view the user information of someone
    url(r'^viewmarket/(?P<session_slug>[\w\-]+)/$', views.show_market_session, name='view_market'), # this is for viewing a session if you're part of the session
    url(r'^begin_haggle/(?P<item_id>[\w\-]+)/$', views.begin_haggle, name="begin_haggle"),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name = 'profile'), # this is required by the django-registration-redux
    url(r'^$', views.index, name='index'),       # I think in the future we should consider redirecting users to userProfile instead of index - Walter 9.3.18
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^add_item/(?P<username>[\w\-]+)/$', views.add_item, name='add_item'),
    url(r'^notifications/(?P<username>[\w\-]+)/$', views.show_notifications, name='notifications'),
    url(r'^api/makeoffer/', views.makeoffer, name="make_offer"),
    url(r'^delete_item/(?P<itemID>[\w\-]+)/$', views.delete_item, name='delete_item'),
    url(r'^delete_offer/(?P<offerID>[\w\-]+)/$', views.delete_offer, name='delete_offer'),
    url(r'^viewoffer/(?P<offerID>[\w\-]+)/$', views.counter_offer, name='counter_offer'),
    url(r'^api/acceptoffer/$', views.accept_offer, name="accept_offer"),
    ]
