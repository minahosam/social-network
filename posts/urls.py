from django.urls import path
from  .views import all_posts , like_or_unlike , postdelete,postupdate
app_name='posts'
urlpatterns = [
    path('',all_posts,name='all'),
    path('like/',like_or_unlike,name='like'),
    path('<pk>/delete',postdelete.as_view(), name='delete'),
    path('<pk>/update',postupdate.as_view(),name='update')
]
