from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
class profile(models.Model):
    first_name = models.CharField(max_length=50,blank=True, null=True)
    last_name=models.CharField(max_length=50,blank=True, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=300,default='no bio........')
    email=models.EmailField(max_length=254,blank=True, null=True)
    country=models.CharField(max_length=50,blank=True, null=True)
    image=models.ImageField(upload_to='images/',default='avatar.jpg')
    friends=models.ManyToManyField(User,related_name='friends',blank=True,null=True)
    slug = models.SlugField(max_length = 50 , unique=True,blank=True, null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateField(auto_now=True)
    def my_friends(self):
        return self.friends.all()
    def my_friends_no(self):
        return self.friends.all().count()
    def __str__(self):
        return str(self.user)
    def save(self, *args, **kwargs):
        if not self.slug:
               self.slug=slugify(self.first_name +' '+self.last_name)
        super(profile, self).save(*args, **kwargs) # Call the real save() method
status_choices=[
    ('sent','sent'),
    ('accepted','accepted'),
    ('rejected','rejected')
]
class relation(models.Model):
    sender = models.ForeignKey(User,related_name='sender', on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,related_name='receiver', on_delete=models.CASCADE)
    status=models.CharField(max_length=10,choices=status_choices)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.sender}--------{self.receiver}'
    