from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Tour, Category
from ..serializers import CategorySerializer, TourFilterSerializer, TourSerializer


@extend_schema(
    methods=['GET'],
    responses={200: TourSerializer(many=True)},
    description='Получить список активных туров',
    parameters=[TourFilterSerializer],
    tags=['Tours'],
)
@extend_schema(
    methods=['POST'],
    request=TourSerializer,
    responses={
        201: TourSerializer,
        400: OpenApiResponse(description='Неверные данные'),
        401: OpenApiResponse(description='Не авторизован'),
    },
    description='Создать новый тур',
    tags=['Tours'],
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def tour_list_create(request):
    if request.method == 'GET':
        tours = Tour.objects.active().prefetch_related('reviews')
        serializer = TourFilterSerializer(data=request.query_params)
        if serializer.is_valid():
            if serializer.validated_data.get('category_id'):
                tours = tours.filter(
                    category_id=serializer.validated_data['category_id']
                )
            if serializer.validated_data.get('min_price'):
                tours = tours.filter(price__gte=serializer.validated_data['min_price'])
            if serializer.validated_data.get('max_price'):
                tours = tours.filter(price__lte=serializer.validated_data['max_price'])
            if serializer.validated_data.get('start_date'):
                tours = tours.filter(
                    start_date__gte=serializer.validated_data['start_date']
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(TourSerializer(tours, many=True).data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['GET'],
    responses={200: CategorySerializer(many=True)},
    description='Получить список всех категорий',
    tags=['Categories'],
)
@extend_schema(
    methods=['POST'],
    request=CategorySerializer,
    responses={
        201: CategorySerializer,
        400: OpenApiResponse(description='Неверные данные'),
        401: OpenApiResponse(description='Не авторизован'),
    },
    description='Создать новую категорию',
    tags=['Categories'],
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TourDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, tour_id):
        return get_object_or_404(Tour, id=tour_id)

    @extend_schema(
        responses={
            200: TourSerializer,
            404: OpenApiResponse(description='Тур не найден'),
        },
        description='Получить детали конкретного тура',
        tags=['Tours'],
    )
    def get(self, request, tour_id):
        tour = self.get_object(tour_id)
        serializer = TourSerializer(tour)
        return Response(serializer.data)

    @extend_schema(
        request=TourSerializer,
        responses={200: TourSerializer, 400: OpenApiResponse(description='Неверные данные')},
        description='Обновить тур (полное обновление)',
        tags=['Tours'],
    )
    def put(self, request, tour_id):
        tour = self.get_object(tour_id)
        serializer = TourSerializer(tour, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=TourSerializer,
        responses={200: TourSerializer, 400: OpenApiResponse(description='Неверные данные')},
        description='Обновить тур (частичное обновление)',
        tags=['Tours'],
    )
    def patch(self, request, tour_id):
        tour = self.get_object(tour_id)
        serializer = TourSerializer(tour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: OpenApiResponse(description='Тур удалён')},
        description='Удалить тур',
        tags=['Tours'],
    )
    def delete(self, request, tour_id):
        tour = self.get_object(tour_id)
        tour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)