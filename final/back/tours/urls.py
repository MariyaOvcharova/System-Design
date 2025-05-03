from django.urls import path

from .views import (
    BookingDetailView,
    BookingListCreateView,
    TourDetailView,
    category_list_create,
    create_review,
    tour_list_create,
)

urlpatterns = [
    path('tours/', tour_list_create, name='tour_list_create'),
    path('tours/<uuid:tour_id>/', TourDetailView.as_view(), name='tour_detail'),
    path('categories/', category_list_create, name='category_list_create'),
    path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
    path(
        'bookings/<uuid:booking_id>/',
        BookingDetailView.as_view(),
        name='booking_detail',
    ),
    path('reviews/', create_review, name='create_review'),
]
