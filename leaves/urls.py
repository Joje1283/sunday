from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeaveCreateView.as_view())
]