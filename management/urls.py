from django.urls import path
from . import views

urlpatterns = [
    path('leaves/', views.LeaveListView.as_view()),
    path('leaves/<int:pk>/', views.LeaveUpdateView.as_view()),
]
