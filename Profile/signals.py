from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profile , relation
@receiver(post_save,sender=User)
def create_profile(sender , instance ,created , **kwargs):
    if created:
        profile.objects.create(User=instance)
@receiver(post_save,sender=relation)
def add_friends(sender,instance,created,**kwargs):
    sender1=instance.sender
    receiver1=instance.receiver
    if instance.status=='accepted':
        sender1.friends.add(sender1.user)
        receiver1.friends.add(receiver1.user)
        sender1.save()
        receiver1.save()