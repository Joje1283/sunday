from django.utils import timezone

from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser

from leaves.models import Use
from .serializers import LeaveSerializer


class LeaveListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Use.objects.filter(cancel=False, end_date__lte=timezone.now())
    serializer_class = LeaveSerializer


class LeaveUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Use.objects.filter(cancel=False, end_date__lte=timezone.now())
    serializer_class = LeaveSerializer
