from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,TemplateView,FormView
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail



class HomeView(View):
    def get(self,request):
        logout(request)
        return render(request,"mainhome.html")
    

    
class RegistrationView(CreateView):
    template_name="reg.html"
    form_class=Regform
    model=User
    success_url=reverse_lazy('login')
    def form_valid(self,form):
        name= form.cleaned_data.get("username")
        password= form.cleaned_data.get("password1")
        send_mail(
                    'Welcome to OpenBlog',
                    f'Thank you for registering with us, Your User Name is: {name} and Password is: {password}',
                    'godwinvinson69@gmail.com',
                    [form.cleaned_data.get("email")]
                )
        self.object=form.save()
        messages.success(self.request,"Registration Succesfull")
        return super().form_valid(form)
    

#<-----------old method---------------->
# class RegistrationView(View):
#     def get(self,request,*args,**kwargs):
#         f=Regform()
#         return render(request,'reg.html',{"form":f})
#     def post(self,request,*args,**kwargs):
#         form_data=Regform(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             messages.success(request,"User registerd Succesfully")
#             return render(request,'mainhome.html',{"form":form_data})
#         else:
#             messages.error(request,"User registration failed")
#             return render(request,'Reg.html',{"form":form_data})
    
class LoginView(FormView):
    template_name="login.html"
    form_class=Logform
    def post(self,request,*args,**kwargs):
        form_data=Logform(data=request.POST)
        if form_data.is_valid():
            un=form_data.cleaned_data.get("username")
            pw=form_data.cleaned_data.get("password")
            user=authenticate(request,username=un,password=pw)
            if user:
                login(request,user)
                return redirect("uhome")
            else:
                messages.error(request,"Enter correct details")
                return redirect("login")
        else:
            return render(request,"login.html",{"form":form_data})
        
        
# class LoginView(View):
#     def get(self,request):
#         f=Logform()
#         return render(request,'login.html',{"form":f})
#     def post(self,request,*args,**kwargs):
#         form_data=Logform(data=request.POST)
#         if form_data.is_valid():
#             un=form_data.cleaned_data.get("username")
#             pw=form_data.cleaned_data.get("password")
#             user=authenticate(request,username=un,password=pw)
#             if user:
#                 return redirect("uhome")
#             else:
#                 messages.error(request,"Enter correct details")
#                 return redirect("login")
#         else:
#             return render(request,"login.html",{"form":form_data})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')