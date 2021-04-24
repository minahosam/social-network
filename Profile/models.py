from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Q
from django.shortcuts import reverse
# Create your models here.
class  profile_manager(models.Manager):
    def all_profiles_exclude_me(self,me):
        all_profile=profile.objects.all().exclude(user=me)
        return all_profile
    def invited_people_aviable(self,me):
        all_profiles=profile.objects.all().exclude(user=me)
        print(all_profiles)
        print('----------------------')
        my_profile=profile.objects.get(user = me)
        print(my_profile)
        print('----------------------')
        qs=relation.objects.filter(Q(sender=me),Q(receiver=me))
        print(qs)
        print('--------------------')
        approved=[]
        for rel in qs:
            if rel.status=='accepted':
                approved.append(rel.sender)
                approved.append(rel.receiver)
        print(approved)
        print('-------------------------')
        aviable_users=[]
        aviable_users=[aviable for aviable in all_profiles if aviable not in approved]
        print(aviable_users)
        print('--------------------')
        return aviable_users
class profile(models.Model):
    first_name = models.CharField(max_length=50,blank=True, null=True)
    last_name=models.CharField(max_length=50,blank=True, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    bio=models.CharField(max_length=300,default='no bio........')
    email=models.EmailField(max_length=254,blank=True, null=True)
    country=models.CharField(max_length=50,blank=True, null=True)
    image=models.ImageField(upload_to='images/',default='avatar.jpg')
    friends=models.ManyToManyField(User,related_name='friends',blank=True,null=True)
    slug = models.SlugField(max_length = 50 , unique=True,blank=True, null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateField(auto_now=True)
    objects=profile_manager()
    def get_absolute_url(self):
        return reverse('profile:detail', kwargs={'slug': self.slug})
    def my_friends(self):
        return self.friends.all()
    def num_posts(self):
        return self.post_author.all().count()
    def all_author_posts(self):
        return self.post_author.all()
    def all_likes_given(self):
        like_num = self.liked_author.all()
        all_likes=0
        for item in like_num:
            if item.value == 'like':
                all_likes += 1
        return all_likes
    def all_likes_received(self):
       all_my_posts= self.post_author.all()
       all_likes=0
       for like in all_my_posts:
           all_likes += like.like_post.all().count()
       return all_likes 
    def my_friends_no(self):
        return self.friends.all().count()
    def __str__(self):
        return str(self.user)
    def save(self, *args, **kwargs):
        if not self.slug:
            if self.first_name and self.last_name:
               self.slug=slugify(self.first_name +' '+self.last_name)
            else:
                self.slug=slugify(self.user)
        super(profile, self).save(*args, **kwargs) # Call the real save() method
status_choices=[
    ('sent','sent'),
    ('accepted','accepted'),
    ('rejected','rejected')
]
# show only received invitation to user
class relationmanager(models.Manager):
    def receive_invitations(self,receiver_):
        received=relation.objects.filter(receiver=receiver_,status='sent')
        return received
    def send_invitations(self,sender_):
        sent=relation.objects.filter(sender=sender_,status='sent')
        return sent
class relation(models.Model):
    sender = models.ForeignKey(User,related_name='sender', on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,related_name='receiver', on_delete=models.CASCADE)
    status=models.CharField(max_length=10,choices=status_choices)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    objects=relationmanager()
    def __str__(self):
        return f'{self.sender}--------{self.receiver}'
    