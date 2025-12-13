from django.urls import path, include
from api import views

urlpatterns = [
    # auth urls
    path('auth/register/', views.RegisterAPIView.as_view(),     name="register"),
    path('auth/login/',    views.LoginAPIView.as_view(),        name="login"),
    path('auth/refresh/',  views.RefreshTokenAPIView.as_view(), name="refresh"),


    # crud urls
    path('tasks/create/',        views.CreateTaskAPIView.as_view(),   name="create_task"), # create a task
    path('tasks/list/',          views.ListTaskAPIView.as_view(),     name="list_tasks"),  # list all tasks
    path('tasks/retrieve/<id>/', views.RetrieveTaskAPIView.as_view(), name="get_task"),    # retrieve a task
    path('tasks/update/<id>/',   views.UpdateTaskAPIView.as_view(),   name="update_task"), # update a task
    path('tasks/delete/<id>/',   views.DeleteTaskAPIView.as_view(),   name="delete_task"), # delete a task

]


