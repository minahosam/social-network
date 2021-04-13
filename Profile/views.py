from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render , redirect
from .models import profile , relation
from .forms import profile_form
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
# Create your views here.
def show_my_profile(request):
    my_profile= profile.objects.get(user=request.user)
    return render(request,'profiles/profile.html',{'profile':my_profile})
def update_profile(request):
    confirm=False
    if request.method=='POST':
        form = profile_form(request.POST,request.FILES)
        if form.is_valid():
            form1=form.save(commit=False)
            form1.user=request.user
            form1
            confirm=True
    else:
        form=profile_form()
    return render(request,'profiles/update.html',{'form':form , 'confirm':confirm})
def invitations_receive(request):
    p=profile.objects.all()
    profile_me= profile.objects.get(user=request.user)
    print(profile_me)
    received=relation.objects.receive_invitations(profile_me.user)
    # print(invite)
    results=list(map(lambda x:x.sender,received))
    # con={'invite':invite}
    print(results)
    is_empty=False
    if len(results)==0:
        is_empty=True
    return render(request,'profiles/invitations.html',{'invite':results , 'is_empty':is_empty,'profile':p})
def accept_invite(request):
    pass
def reject_invite(request):
    pass
def invitation_sent(request):
    invite_sent=relation.objects.send_invitations(request.user)
    con={'sent':invite_sent}
    return render(request,'profiles/sent_invitations.html',con)
def all_aviable_profiles(request):
    all_profiles=profile.objects.all_profiles_exclude_me(request.user)
    return render(request,'profiles/aviable_profiles.html',{'aviable':all_profiles})
def aviable_invited_people(request):
    aviable_profiles=profile.objects.invited_people_aviable(request.user)
    return render(request,'profiles/aviable_prodiles.html',{'aviable':aviable_profiles})
class all_profiles(ListView):
    model=profile
    template_name='profiles/all.html'
    context_object_name='qs'
    def get_queryset(self):
        qs=profile.objects.all_profiles_exclude_me(self.request.user)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Cannot use QuerySet for "profile": Use a QuerySet for "User"
        user=User.objects.get(username__iexact=self.request.user)
        user_profile=profile.objects.get(user=user)
        rel_r=relation.objects.filter(sender=self.request.user)
        rel_s=relation.objects.filter(receiver=self.request.user)
        rel_receiver=[]
        rel_sender=[]
        for item in rel_r:
            rel_receiver.append(item.receiver)
        for item in rel_s:
            rel_sender.append(item.sender)
        context['rel_receiver']=rel_receiver
        context['rel_sender']=rel_sender
        context['is_empty']=False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context
def send_invitation(request):
    if request.method=='GET':
        pk=request.GET.get('profile_pk')
        user=request.user
        print(user)
        user_send_invitation=profile.objects.get(user=user)
        print(user_send_invitation)
        send_invite_to=profile.objects.get(pk=pk)
        print(send_invite_to)
        user_invited=send_invite_to.user
        print(user_invited)
        rel=relation.objects.create(sender=user,receiver=user_invited,status='sent')
        # return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:all')
def remove_user(request):
    if request.method =='GET':
        pk=request.GET.get('profile_pk')
        user=request.user
        user_want_to_delete=profile.objects.get(pk=pk)
        delete_user=user_want_to_delete.user
        rel=relation.objects.get(Q(sender=user)&Q(receiver=delete_user)| Q(receiver=user)&Q(sender=delete_user))
        rel.delete()
    return redirect('profile:all')