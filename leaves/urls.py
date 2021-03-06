from django.urls import path
from . import views

"""
1번 유저에 대한 휴가 생성
/accounts/1/leave/grant
인증된 유저가 휴가를 사용
/leave/use
"""

urlpatterns = [
    path('', views.leave_history_view),
    path('grant/', views.GrantCreateView.as_view()),  # /accounts/<user_id>/grant
    path('use/', views.UseCreateView.as_view()),  # /use
    path('count/', views.use_count_view),
    path('use/<int:pk>/', views.UseUpdateView.as_view())
]
