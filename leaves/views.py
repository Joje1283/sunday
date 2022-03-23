from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView

from .models import Use, Type
from .serializers import (
    UseCreateSerializer,
    GrantSerializer,
    get_residual_leave_count,
    LeaveCountSerializer,
    UseSerializer,
    LeaveHistorySerializer,
)


class UseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UseCreateSerializer

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
        serializer = UseCreateSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            result = serializer.result
            result['user'] = request.user
            Use.objects.create(**result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UseCancelView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UseSerializer
    queryset = Use.objects.all()


class GrantCreateView(CreateAPIView):
    serializer_class = GrantSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        target_user_id = self.request.parser_context['kwargs']['pk']
        serializer.save(user_id=target_user_id)
        return super().perform_create(serializer)


@api_view(['GET'])
def use_count_view(request):
    if request.query_params and request.query_params.get('type'):
        type = request.query_params.get('type')
        leave_count = get_residual_leave_count(request.user.pk, type)
    else:
        leave_count = get_residual_leave_count(request.user.pk, Type.ANNURE)
    serializer = LeaveCountSerializer({'count': leave_count})
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_history_view(request):
    user = request.user
    type = request.query_params.get('type')
    use_qs = Use.objects.filter(user=user)
    if type == 'reserved':
        use_qs = use_qs.filter(approve=True)
    serializer = LeaveHistorySerializer(use_qs, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

