from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profile , relation
@receiver(post_save,sender=User)
def create_profile(sender , instance ,created , **kwargs):
    if created:
        profile.objects.create(user=instance)
@receiver(post_save,sender=relation)
def add_friends(sender,instance,created,**kwargs):
    sender_=instance.sender
    receiver_=instance.receiver
    # user=instance.user
    if instance.status=='accepted':
        receiver_.friends.add(sender_.user)
        sender_.friends.add(receiver_.user)
        sender_.save()
        receiver_.save()
@receiver(pre_delete,sender=relation)
def remove_friends(sender,instance,**kwargs):
    sender_=instance.sender
    receiver_=instance.receiver
    sender_.friends.remove(receiver_.user)
    receiver_.friends.remove(sender_.user)
    sender_.save()
    receiver_.save()
@receiver(post_save,sender=relation)
def reject_friends(sender,instance,created, **kwargs):
    sender_=instance.sender
    receiver_=instance.receiver
    if  isinstance.status=='rejected':
        sender_.friends.remove(receiver_.user)
        receiver_.friends.remove(sender_.user)
        sender_.save()
        receiver_.save()