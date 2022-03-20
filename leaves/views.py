from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from .models import Use
from .serializers import UseSerializer, GrantSerializer


class UseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UseSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def post(self, request, format=None):
        serializer = UseSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            result = serializer.result
            result['user'] = request.user
            Use.objects.create(**result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GrantCreateView(CreateAPIView):
    serializer_class = GrantSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        target_user_id = self.request.parser_context['kwargs']['pk']
        serializer.save(user_id=target_user_id)
        return super().perform_create(serializer)
