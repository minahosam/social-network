from django.urls import path
from .views import send_invitation, show_my_profile,update_profile , invitations_receive,invitation_sent,all_aviable_profiles,aviable_invited_people,all_profiles,send_invitation,remove_user,accept_invite,reject_invite,profile_detail
app_name='profile'
urlpatterns = [
    path('',show_my_profile,name='my_profile'),
    path('update/',update_profile,name='update'),
    path('invite/',invitations_receive,name='invite'),
    path('sent/',invitation_sent,name='sent_'),
    path('all_profiles/',all_aviable_profiles,name='all'),
    path('aviable_prof',aviable_invited_people,name='available'),
    path('all/',all_profiles.as_view(),name='all'),
    path('sent-invitation/',send_invitation,name='sent'),
    path('remove-user/',remove_user,name='remove'),
    path('accept/',accept_invite,name='accept'),
    path('reject/',reject_invite,name='reject'),
    path('<slug>/',profile_detail.as_view(),name='detail'),
]
