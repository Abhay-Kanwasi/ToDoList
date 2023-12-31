# Default 
from django.shortcuts import render

# imported from built-in django modules
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from django.shortcuts import redirect

# imported from this app
from .models import Task


class Base_Login(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class Base_Register(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm   # redering this form in register.html form.as_p
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Base_Register, self).form_valid(form)
    
    # restrict login user to login again
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Base_Register, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):   # LoginRequiredMixin will check login but redirect user to default not login page so we have to set it and Listview return a template with query set of data
    model = Task
    context_object_name = 'tasks'   #change the object list to tasks

    # ensure user can only get their data nor another user data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # context set to orignal value | get_context_data making sure we are inheriting from the orignal item
        context['tasks'] = context['tasks'].filter(user=self.request.user) # Filtering tasks according to user who created them
        context['count'] = context['tasks'].filter(complete=False).count()   # count of incomplete items
        
        search_input = self.request.GET.get('search-area') or '' # whatever user search it will get the value and default value is empty string('')
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)
        
        context['search_input'] = search_input  # whatever user search it will add into template using as value
        return context
    template_name = 'base/tasks.html'

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'quote']
    success_url = reverse_lazy('tasks')  # it redirect's our user to a certain page
    template_name = 'base/create.html'

    def form_valid(self, form): # overriding the value so user set default not give option of choosing user to add task
        form.instance.user = self.request.user  # ensure that it's logined user
        return super(TaskCreate, self).form_valid(form) 

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'quote']
    success_url = reverse_lazy('tasks')  # it redirect's our user to a certain page
    template_name = 'base/create.html'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')  # it redirect's our user to a certain page
    template_name = 'base/delete.html'

