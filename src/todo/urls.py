from django.urls import path

from todo.views import TaskList, CustomLoginView, CustomLogoutView, AddTask, TaskDetail, TaskUpdate, TaskDelete, HistoryList, TaskCompleted, HistoryClean, TaskIncompleted, SignUpView


urlpatterns = [
    path('', TaskList.as_view(), name='task_list'),
    path('task/add/', AddTask.as_view(), name='add_task'),
    path("history/", HistoryList.as_view(), name="history"),
    path("history/clean/", HistoryClean.as_view(), name="history_clean"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/completed/', TaskCompleted.as_view(), name='task_completed'),
    path('task/<int:pk>/incomplete/', TaskIncompleted.as_view(), name='task_incompleted'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
]
