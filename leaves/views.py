from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UseSerializer
from .models import Use


class LeaveCreateView(APIView):
    def post(self, request, format=None):
        serializer = UseSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.result
            result['user'] = get_user_model().objects.first()  # Todo: Login User로 변경
            Use.objects.create(**result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
