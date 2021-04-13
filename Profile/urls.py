from django.urls import path
from .views import send_invitation, show_my_profile,update_profile , invitations_receive,invitation_sent,all_aviable_profiles,aviable_invited_people,all_profiles,send_invitation,remove_user
app_name='profile'
urlpatterns = [
    path('',show_my_profile,name='my_profile'),
    path('update/',update_profile,name='update'),
    path('invite/',invitations_receive,name='invite'),
    path('sent/',invitation_sent,name='sent'),
    path('all_profiles/',all_aviable_profiles,name='all'),
    path('aviable_prof',aviable_invited_people,name='available'),
    path('all/',all_profiles.as_view(),name='all'),
    path('sent-invitation/',send_invitation,name='sent'),
    path('remove-user/',remove_user,name='remove'),
]
