from django.utils import timezone

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from leaves.models import Use
from .serializers import LeaveListSerializer


class LeaveListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Use.objects.filter(cancel=False, approve=False, end_date__lte=timezone.now())
    serializer_class = LeaveListSerializer

