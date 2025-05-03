import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TourManager(models.Manager):
    def active(self):
        now = timezone.now()
        return self.filter(is_active=True, start_date__lte=now, end_date__gte=now)


class Tour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='tours'
    )
    is_active = models.BooleanField(default=True)
    photo_urls = models.JSONField(default=list, blank=True)
    objects = TourManager()

    def __str__(self):
        return self.name
    
    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = round(avg_rating, 1)
        else:
            self.rating = 0.0
        self.save()



class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(
        max_length=20,
        choices=[
            ('confirmed', 'Confirmed'),
            ('pending', 'Pending'),
            ('canceled', 'Canceled'),
        ],
        default='pending',
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tour'], name='unique_user_tour_booking')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.tour.name}'


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tour.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.tour.update_rating()

    def __str__(self):
        return f'{self.user.username} - {self.tour.name} - {self.rating}'
