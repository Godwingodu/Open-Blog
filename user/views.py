from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView,UpdateView,DeleteView
from django.http import HttpResponse
from account.models import UserProfile
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from account.forms import *
from django.contrib.auth import authenticate,logout
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404



def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            return redirect('login')
    return wrapper  


@method_decorator(signin_required,name='dispatch')
class Uhome(CreateView):
    template_name="userhome.html"
    model=Comments
    form_class=CommentForm
    success_url=reverse_lazy('uhome')
    def get_context_data(self,**kwargs) :
        context=super().get_context_data(**kwargs)
        context["comment"]=Comments.objects.all()
        context["users"]=User.objects.all().exclude(username=self.request.user.username)
        following = follows.objects.filter(followers=self.request.user).values_list('user',flat=True) #output will be in in query format
        lists = list(following) #so conert it in to lists
        lists.append(self.request.user.id) #we want to add the my blogs in userhome,so we want to append in lists
        context['following'] = User.objects.filter(id__in=following)
        if self.request.method == 'GET': # this will be GET now      
            searchinput =  self.request.GET.get('search') or '' # do some research what it does       
            if searchinput:
                context["data"]=Blogs.objects.filter(title__icontains=searchinput,user_id__in=lists)
            else:
                context["data"]=Blogs.objects.filter(user_id__in=lists).order_by('-date')
        context['searchinput'] = searchinput
        return context


def Comment(request,*args,**kwargs):
    if request.method=="POST":
        bid=kwargs.get("bid")
        blog=Blogs.objects.get(id=bid)
        user=request.user
        comment=request.POST.get("comment")
        Comments.objects.create(comment=comment,user=user,blog=blog)
        messages.success(request,"Comment added successfully")
        return redirect("uhome")


@method_decorator(signin_required,name='dispatch')
class UserProfiles(TemplateView):
    template_name="profile.html"
    def get_context_data(self,**kwargs) :
        context=super().get_context_data(**kwargs)
        context["post"]=Blogs.objects.filter(user_id=self.request.user).count()
        context["followers"]=follows.objects.filter(followers_id=self.request.user).count()
        context["following"]=follows.objects.filter(user_id=self.request.user).count()
        return context
  

@method_decorator(signin_required,name='dispatch')
class AddProfile(CreateView):
    template_name="addprofile.html"
    form_class=ProfileForm
    model=UserProfile
    success_url=reverse_lazy('uprofile')
    def form_valid(self,form) :
        form.instance.user=self.request.user
        self.object=form.save()
        messages.success(self.request,"profile added succesfully")
        return super().form_valid(form)
    
    
    #<----------------add profile old post method------------------->
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(data=request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         return redirect('uprofile')
    #     else:
    #         return render(request,"addprofile.html",{"form":form})



@method_decorator(signin_required,name='dispatch')
class ChangePassword(FormView):
    template_name="changepassword.html"
    form_class=ChangePassword
    def post(self,request,*args,**kwargs):
        form=self.form_class(data=request.POST)
        if form.is_valid():
            old=form.cleaned_data.get("oldpassword")
            new=form.cleaned_data.get("newpassword")
            cnf=form.cleaned_data.get("confirmpassword")
            user=authenticate(request,username=request.user.username,password=old)
            if user:
                if new==cnf:
                    # user.password=new
                    user.set_password(new)
                    user.save()
                    logout(request)
                    messages.success(request,"Password changed Succesfully")
                    return redirect("login")
                else:
                    messages.error(request,"Password Mismatch")
                    return redirect("changepassword")
            else:
                messages.error(request,"Old password entered is incorrect")
                return redirect("changepassword")
       


        

@method_decorator(signin_required,name='dispatch')
class UpdateProfile(UpdateView):
    template_name="updateprofile.html"
    form_class=ProfileForm
    model=UserProfile
    success_url=reverse_lazy('uprofile')
    pk_url_kwarg="pk"
    def form_valid(self,form):
        self.object=form.save()
        messages.success(self.request,"Profile Updated Succesfully")
        return super().form_valid(form)
    

#<----------------update profile old method------------------->
# class UpdateProfile(View):
#     def get(self,request,*args,**kwargs):
#         pid=kwargs.get("pid")
#         p=UserProfile.objects.get(id=pid)
#         f=ProfileForm(instance=p)
#         return render(request,"updateprofile.html",{"form":f})
#     def post(self,request,*args,**kwargs):
#         pid=kwargs.get("pid")
#         p=UserProfile.objects.get(id=pid)
#         form_data=ProfileForm(data=request.POST,files=request.FILES,instance=p)
#         if form_data.is_valid:
#             form_data.save()
#             messages.success(request,"Profile Updated") 
#             return redirect("uprofile")
#         else:
#             return render(request,"updateprofile.html",{"form":form_data})
    


@method_decorator(signin_required,name='dispatch')
class AddBlogView(CreateView):
    template_name="addblog.html"
    form_class=AddBlogForm
    model=Blogs
    success_url=reverse_lazy('uhome')
    def form_valid(self,form):
        if form.is_valid():
            form.instance.user=self.request.user
            self.object=form.save()
            messages.success(self.request,"Blog posted succesfully")
            return super().form_valid(form)
        


@method_decorator(signin_required,name='dispatch')
class MyBlogsView(View):
    def get(self,request,*args,**kwargs):
        f=Blogs.objects.filter(user=request.user).order_by("-date")
        return render(request,"myblogs.html",{"form":f})
    



@method_decorator(signin_required,name='dispatch')        
class EditBlogsView(UpdateView):
    template_name="editblogs.html"
    model=Blogs
    form_class=AddBlogForm
    success_url=reverse_lazy('myblogs')



@method_decorator(signin_required,name='dispatch') 
class DeleteBlogsView(DeleteView):
    template_name="deleteblogs.html"
    model=Blogs
    success_url=reverse_lazy('myblogs')



def AddLike(request,*args,**kwargs):
    bid=kwargs.get("id")
    blog=Blogs.objects.get(id=bid)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect('uhome')



def RemoveLike(request,*args,**kwargs):
    bid=kwargs.get("id")
    blog=Blogs.objects.get(id=bid)
    blog.liked_by.remove(request.user)
    blog.save()
    return redirect('uhome')




def Follow(request,id):
    if follows.objects.filter(followers_id=request.user.id , user_id=id).exists():
        followObj = follows.objects.filter(followers_id=request.user.id , user_id=id)
        followObj.delete()
    else:
        user = User.objects.get(id=id)  
        followObj = follows.objects.create(followers_id=request.user.id , user_id=user.id) 
        followObj.save()  
        print(request.path)
    url = request.META.get('HTTP_REFERER') ##used to get current url
    if 'allusersprofile' in url:
        return redirect(url)
    else:
        return redirect('uhome')




@method_decorator(signin_required,name='dispatch')
class AllUsersProfile(TemplateView):
    template_name="allusersprofile.html"
    def get_context_data(self,**kwargs) :
        uid=kwargs.get("id")
        context=super().get_context_data(**kwargs)
        context["usersp"]=User.objects.filter(id=uid)
        context["post"]=Blogs.objects.filter(user_id=uid).count()
        context["followers"]=follows.objects.filter(followers_id=uid).count()
        context["following"]=follows.objects.filter(user_id=uid).count()
        following = follows.objects.filter(followers=self.request.user).values_list('user',flat=True)
        context['followinguser'] = User.objects.filter(id__in=following)
        return context