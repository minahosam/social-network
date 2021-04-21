from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import post , like
from Profile.models import profile
from .forms import  PostForm,CommentForm
from django.views.generic import UpdateView,DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def all_posts(request):
    posts=post.objects.all()
    user=profile.objects.get(user=request.user)
    if request.method=='POST':
        form_p=PostForm(request.POST,request.FILES)
        if form_p.is_valid():
            instance=form_p.save(commit=False)
            instance.author=user
            instance.save()
            return redirect('posts:all')
    else:
        form_p=PostForm()
    if request.method=='POST':
        form_c=CommentForm(request.POST,request.FILES)
        query1=request.POST.get('q')
        print(query1)        
        post_according_to_query=post.objects.get(id=query1)
        if form_c.is_valid():
            instance=form_c.save(commit=False)
            instance.author=user
            instance.commented_post=post_according_to_query
            instance.save()
            return redirect('posts:all')
    else:
        form_c=CommentForm()
    return render(request,'posts/all_post.html',{'posts':posts , 'user':user ,'form_p':form_p , 'form_c':form_c})
@login_required
def like_or_unlike(request):
    user=request.user
    print(user)
    if request.method=='POST':
        global query
        query=request.POST.get('query')
        print(query)
        post_query=post.objects.get(id=query)
        get_user=profile.objects.get(user=user)
        if get_user in post_query.like_post.all():
            post_query.like_post.remove(get_user)
        else:
            post_query.like_post.add(get_user)
        likee ,created=like.objects.get_or_create(like_author=get_user,liked_post=post_query)
        if  not created:
            if likee.value=='like':
                likee.value='unlike'
            else:
                likee.value='like'
        else:
            if likee.value=='like':
                likee.value='unlike'
            else:
                likee.value='like'
            likee.save()
            post_query.save()
        data={
            'value':likee.value,
            'likes':post_query.like_post.all().count()
        }
        return JsonResponse(data,safe=False)
    return redirect('posts:all')
class postdelete(LoginRequiredMixin,DeleteView):
    model = post
    template_name ='posts/delete_post.html'
    # success_url ='/posts/'
    success_url = reverse_lazy('posts:all')
    def get_object(self,*args,**kwargs):
        pk=self.kwargs.get('pk')
        delete_post=post.objects.get(pk=pk)
        if not self.request.user == delete_post.author.user:
            messages.warning(self.request,'you cannot delete this post')
        return delete_post
class postupdate(LoginRequiredMixin,UpdateView):
    model = post
    form_class=PostForm
    template_name='posts/update.html'
    success_url=reverse_lazy('posts:all')
    # def get_object(self,*args,**kwargs):
    #     pk=self.kwargs.get('pk')
    #     update_post=post.objects.get(pk=pk)
        # if self.request.user==update_post.author.user:
        #     return super().form_valid(form)
        # else:
        #     messages.warning(self.request,'you cannot update this post')
        # return update_post
        # correct code below
        # if not self.request.user==update_post.author.user:
        #     messages.warning(self.request,'you cannot update')
        # return update_post
        # another soluation
    def form_valid(self, form):
        user=profile.objects.get(user=self.request.user)
        if form.instance.author ==user:
            return super().form_valid(form)
        else:
            form.add_error(None,'you cannot update')
            return super().form_invalid(form)