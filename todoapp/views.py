from django.shortcuts import render,redirect
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic import View,TemplateView,CreateView,ListView,DetailView,UpdateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todoapp.models import Todos
from django.contrib import messages
from todoapp.decorators import signin_required
from django.utils.decorators import method_decorator
@method_decorator(signin_required,name="dispatch")
class SignupView(CreateView):

    model = User
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")       #auth created userine create cheyan ulla method forms usercreation form

    def form_valid(self, form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)

    # def get(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm()
    #     return render(request,"registration.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         return redirect("signin")#login name ane signin, register redirect to loginpage
    #     else:
    #         return ("registeration.html",{"form":form})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                messages.success(request,"created account")
            return redirect("index")

        else:

            messages.error(request,"invalid credentials")
            return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["todos"]=Todos.objects.filter(user=self.request.user,status=False)
        return context

    # def get(self,request,*args,**kwargs):
    #     return render(request,"home.html")

@method_decorator(signin_required,name="dispatch")
class signoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

# todo create cheyan view
@method_decorator(signin_required,name="dispatch")
class TodoAddView(CreateView):
    model = Todos
    form_class = forms.TdoForm
    template_name = "add-todo.html"
    success_url = reverse_lazy("todos-list")



    def form_valid(self, form):            #form instancelot user addchyan
        form.instance.user=self.request.user
        messages.success(self.request,"create todos")
        return super().form_valid(form)




    # def get(self,request,*args,**kwargs):
    #     form=forms.TdoForm()
    #     return render(request,"add-todo.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form=forms.TdoForm(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user      #userine passcheyunnform instance ane Todo only work modelform
    #         #Todos.objects.create(**form.cleaned_data,user=request.user)
    #         form.save()
    #         messages.success(request,"added todo")
    #         return redirect("index")
    #     else:
    #         messages.error(request,"not created")
    #         return render(request,"add-todo.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class TodosList(ListView):
    model = Todos
    context_object_name = "todos"
    template_name = "todolist.html"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)#custom query set write cheyan get queryset overrid cheyanam

    # def get(self,request,*args,**kwargs):
    #     all_todos=Todos.objects.filter(user=request.user)
    #     return render(request,"todolist.html",{"todos":all_todos})

# localhost:8000/todos/remove/<int:id>
@signin_required
def delete_todo(request,*args,**kwargs):
    print(request.user.is_authenticated)
    id=kwargs.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("todos-list")
@method_decorator(signin_required,name="dispatch")
class TodoDetailView(DetailView):
    model = Todos
    context_object_name = "todo"
    template_name = "todo-detail.html"      #object
    pk_url_kwarg = "id"

    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todos=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":todos})
@method_decorator(signin_required,name="dispatch")
class TodoEditView(UpdateView):
    model = Todos
    form_class = forms.TodoChangeForm
    template_name = "todo-edit.html"
    success_url = reverse_lazy("index")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        messages.success(self.request,"todo has been changed")
        return super().form_valid(form)

    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(instance=todo)
    #     return render(request,"todo-edit.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(request.POST,instance=todo)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "todo has been changed")
    #         return redirect("todos-list")

        # else:
        #     messages.error(request,"todo update failed")
        #     return render(request,"todo-edit",{"form":form})
