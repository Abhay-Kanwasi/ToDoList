# Default 
from django.shortcuts import render

# imported from built-in django modules
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# imported from this app
from .models import Task


class Base_Login(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):   # LoginRequiredMixin will check login but redirect user to default not login page so we have to set it and Listview return a template with query set of data
    model = Task
    context_object_name = 'tasks'   #change the object list to tasks

    # ensure user can only get their data nor another user data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # context set to orignal value | get_context_data making sure we are inheriting from the orignal item
        context['tasks'] = context['tasks'].filter(user=self.request.user) # Filtering tasks according to user who created them
        context['count'] = context['tasks'].filter(complete=False).count()   # count of incomplete items
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

