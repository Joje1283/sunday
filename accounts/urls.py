from django.urls import path, include

urlpatterns = [
    path('<int:pk>/leaves/', include('leaves.urls'))
]