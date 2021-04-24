from .models import profile , relation
def user_pic(request):
    if request.user.is_authenticated:
        my_profile=profile.objects.get(user=request.user)
        # pic=my_profile.image
        return{'profile':my_profile}
    return{}
def invitation_receive_no(request):
    if request.user.is_authenticated:
        invitations_num=relation.objects.receive_invitations(receiver_=request.user).count()
        return{'inv_num':invitations_num}
    return{}