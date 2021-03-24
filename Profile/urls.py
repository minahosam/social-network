from django.urls import path
from .views import show_my_profile,update_profile
app_name='profile'
urlpatterns = [
    path('',show_my_profile,name='my_profile'),
    path('update/',update_profile,name='update'),
]