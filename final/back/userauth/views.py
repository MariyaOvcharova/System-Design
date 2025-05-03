from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={
        201: RegisterSerializer,
        400: OpenApiResponse(description='Неверные данные'),
    },
    description='Зарегистрировать нового пользователя',
    tags=['Auth'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Успешный выход'),
            401: OpenApiResponse(description='Не авторизован'),
        },
        description='Выход пользователя (инвалидация токена)',
        tags=['Auth'],
    )
    def post(self, request):
        return Response(
            {'message': 'Successfully logged out'}, status=status.HTTP_200_OK
        )
