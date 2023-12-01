from django.shortcuts import render,redirect

from django.views.generic import View
from reminder.forms import UserForm,LoginForm,TodoForm
from django.contrib.auth import authenticate,login,logout 
from reminder.models import Todos


from django.views.decorators.cache import never_cache

from django.utils.decorators import method_decorator

from django.contrib import messages
# Create your views here.



def singin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
             messages.error(request,"failed to login")
             return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper



decs=[singin_required,never_cache]

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("account created")
            return redirect("register")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})
        
class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("login sucess")
                return redirect("index")
        print("invalid")
        return render(request,"login.html",{"form":form})
    
@method_decorator(decs,name="dispatch")
class IndexView(View):
   def get(self,request,*args,**kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})
   
   def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"index.html",{"form":form})
        
@method_decorator(decs,name="dispatch")       
class TodoDeleteView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()

        return redirect("index")
    
@method_decorator(decs,name="dispatch")        
class TodoChangeView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.status==True:
            todo_object.status=False
            todo_object.save()
        else:
            todo_object.status=True
            todo_object.save()
        return redirect("index")
    
@method_decorator(decs,name="dispatch")
class SingOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin") 