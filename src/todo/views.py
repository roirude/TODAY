from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from todo.models import Task, History


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    ordering = ['-date_created']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        if search_query:
             queryset = queryset.filter(user=self.request.user, complete=False, title__icontains=search_query)
        else:
            queryset = queryset.filter(user=self.request.user, complete=False)
        return queryset
    
       
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name ='task'
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'todo/task_update.html'
    fields = ['title', 'description', 'complete']
    
    def get_success_url(self):
        return reverse_lazy('task_list')
    

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    
    def get_success_url(self):
        return reverse_lazy('task_list')
    
    
class TaskCompleted(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.complete = True
        history = History.objects.create(task_completed=task)
        task.save()
        history.save()
        return redirect('task_list')
    
    
class TaskIncompleted(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.complete = False
        history = History.objects.get(task_completed=task)
        history.delete()
        task.save()
        return redirect('history')
        
    
class AddTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'todo/add_task.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('task_list')
    
    
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task_list')
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('task_list')
        return super().get(request, *args, **kwargs)
    
    
class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')
    
    
class SignUpView(FormView):
    form_class = UserCreationForm
    template_name = 'todo/signup.html'
    success_url = reverse_lazy('task_list')
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpView, self).form_valid(form)
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('task_list')
        return super().get(request, *args, **kwargs)
    
    
    
    
# History managment
class HistoryList(LoginRequiredMixin, ListView):
    model = History
    template_name = 'history_list.html'
    context_object_name = 'histories'
    ordering = ['-date_complete']
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(task_completed__user=self.request.user, task_completed__title__icontains=search_query)
        else:
            queryset = queryset.filter(task_completed__user=self.request.user)
        return queryset
    

class HistoryClean(LoginRequiredMixin, View):
    def get(self, request):
        tasks = Task.objects.filter(user=self.request.user, complete=True)
        tasks.delete()
        return redirect('history')