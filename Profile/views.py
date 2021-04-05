from django.shortcuts import render
from .models import profile , relation
from .forms import profile_form
from django.shortcuts import get_object_or_404
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
    # profile_me= profile.objects.get(user=request.user)
    # print(profile_me)
    invite=relation.objects.receive_invitations(request.user)
    print(invite)
    con={'invite':invite}
    return render(request,'profiles/invitations.html',{'invite':invite})