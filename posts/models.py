from django.db import models
from django.contrib.auth.models import User
from Profile.models import profile
from django.core.validators import FileExtensionValidator
# Create your models here.
class post(models.Model):
    content=models.TextField()
    image = models.ImageField(upload_to='post_image/',blank=True, null=True,validators=[FileExtensionValidator(['png','jpg','jepg'])])
    author=models.ForeignKey(profile,related_name='post_author',on_delete=models.CASCADE)
    like_post=models.ManyToManyField(profile,related_name='like_post',blank=True,null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    def num_of_comments(self):
        return self.commented_post.all().count()
        # return self.comment_set.all().count()------modelname_set
    def __str__(self):
        return f'{self.content}---{self.created}'
    def no_of_like(self):
        return self.like_post.all().count()
    class Meta:
        ordering=['-created',]
class comment(models.Model):
    comment_content=models.TextField()
    image = models.ImageField(upload_to='comment_image/',blank=True, null=True,validators=[FileExtensionValidator(['jpg','png','jepg'])])
    author=models.ForeignKey(profile,related_name='comment_author',on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    commented_post=models.ForeignKey(post,related_name='commented_post',on_delete=models.CASCADE)
    def __str__(self):
        return self.comment_content[:10]
    class Meta:
        ordering=['created',]
liked_value=(
    ('like','like'),
    ('unlike','unlike')
)
class like(models.Model):
    value=models.CharField(max_length=7,choices=liked_value)
    like_author=models.ForeignKey(profile,related_name='liked_author',on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    liked_post=models.ForeignKey(post,related_name='liked_post',on_delete=models.CASCADE)    
    def __str__(self):
        return f'{self.value}---------str{self.like_author}'