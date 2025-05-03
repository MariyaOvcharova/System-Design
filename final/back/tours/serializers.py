import uuid

import boto3
from backend import settings
from rest_framework import serializers

from .models import Booking, Category, Review, Tour


class TourFilterSerializer(serializers.Serializer):
    category_id = serializers.UUIDField(required=False)
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    max_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    start_date = serializers.DateTimeField(required=False)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour = serializers.UUIDField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'tour', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        tour_uuid = validated_data.pop('tour')
        tour = Tour.objects.get(id=tour_uuid)
        review = Review.objects.create(tour=tour, **validated_data)
        return review


class TourSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    photos = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    photo_urls = serializers.ListField(child=serializers.URLField(), read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id',
            'name',
            'description',
            'price',
            'start_date',
            'end_date',
            'rating',
            'category',
            'category_id',
            'is_active',
            'reviews',
            'photos',
            'photo_urls',
        ]
        read_only_fields = ['is_active', 'photo_urls']

    def create(self, validated_data):

        photos = validated_data.pop('photos', [])

        tour = Tour.objects.create(**validated_data)

        if photos:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            photo_urls = []

            for photo in photos:

                file_name = f'tours/{tour.id}/{uuid.uuid4()}{photo.name}'

                s3_client.upload_fileobj(
                    photo,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    file_name,
                    ExtraArgs={'ACL': 'public-read'},
                )

                photo_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}'
                photo_urls.append(photo_url)

            tour.photo_urls = photo_urls
            tour.save()

        return tour


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour = TourSerializer(read_only=True)
    tour_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'tour', 'tour_id', 'booking_date', 'status']
        read_only_fields = ['user', 'booking_date', 'tour_id']
