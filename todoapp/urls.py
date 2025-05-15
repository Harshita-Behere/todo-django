#app's url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/',views.login_view, name = 'login'),
    path('todo/',views.todo, name = 'todo'),
     path('edit/<int:sr>/', views.edit_task, name='edit-task'),
    path('delete/<int:sr>/', views.delete_task, name='delete-task'),
]
