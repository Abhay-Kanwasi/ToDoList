# Default 
from django.shortcuts import render

# imported from built-in django modules
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# imported from this app
from .models import Task


class Base_Login(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(ListView):   # Listview return a template with query set of data
    model = Task
    context_object_name = 'tasks'   #change the object list to tasks
    template_name = 'base/tasks.html'

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'  # include all the fields of the model
    success_url = reverse_lazy('tasks')  # it redirect's our user to a certain page
    template_name = 'base/create.html'

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'  # include all the fields of the model
    success_url = reverse_lazy('tasks')  # it redirect's our user to a certain page
    template_name = 'base/create.html'

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')  # it redirect's our user to a certain page
    template_name = 'base/delete.html'

