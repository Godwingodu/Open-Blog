from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    age=models.IntegerField()
    bio=models.CharField(max_length=100,null=True)
    options=(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    gender=models.CharField(choices=options,max_length=100,default="Other")
    phone=models.IntegerField()
    profile_pic=models.ImageField(upload_to="profile_pictures")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="p_user")


class Blogs(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)
    image=models.ImageField(upload_to="blog_images")
    date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog")
    liked_by=models.ManyToManyField(User,related_name="likes",null=True)

    @property
    def alllikes(self):
        return self.liked_by.all()
    
    @property
    def liked_users(self):
        users=self.liked_by.all()
        res=[ user.username for user in users]
        return res



class Comments(models.Model):
    comment=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE,related_name="c_blog")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="c_user")

class follows(models.Model):
    followers=models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,null=True)

