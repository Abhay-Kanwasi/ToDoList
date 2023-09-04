from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, Base_Login, Base_Register

urlpatterns = [

    # loggin urls
    path('login/', Base_Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name="logout"),
    path('register/', Base_Register.as_view(), name='register'),
    
    # actions urls
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
    path('create-task/',TaskCreate.as_view(), name='create-task'),
    path('update-task/<int:pk>/',TaskUpdate.as_view(), name='update-task'),
    path('delete-task/<int:pk>/',TaskDelete.as_view(), name='delete-task'),
    
]