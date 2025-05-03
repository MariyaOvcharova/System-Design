import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TourService } from '../../services/tour.service';
import { BookingService } from '../../services/booking.service';
import { ReviewService } from '../../services/review.service';
import { AuthService } from '../../services/auth.service';
import { Tour } from '../../models/tour.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-tour-info',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tour-info.component.html',
})
export class TourInfoComponent {
  tour: Tour | null = null;
  loading: boolean = true;
  rating: number = 1;
  comment: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private tourService: TourService,
    private bookingService: BookingService,
    private reviewService: ReviewService,
    private authService: AuthService
  ) {
    const tourId = this.route.snapshot.paramMap.get('id');
    if (tourId) {
      this.tourService.getTourById(tourId).subscribe({
        next: (tour) => {
          this.tour = tour;
          this.loading = false;
        },
        error: (err) => {
          console.error('Failed to fetch tour:', err);
          this.loading = false;
        },
      });
    }
  }

  bookTour(): void {
    this.authService.isAuthenticated().subscribe((isAuthenticated) => {
      if (!isAuthenticated) {
        this.router.navigate(['/login']);
        return;
      }
      if (this.tour) {
        this.bookingService.createBooking({ tour_id: this.tour.id }).subscribe({
          next: () => {
            alert('Booking created successfully!');
          },
          error: (err) => {
            alert('Failed to create booking');
          },
        });
      }
    });
  }

  submitReview(): void {
    this.authService.isAuthenticated().subscribe((isAuthenticated) => {
      if (!isAuthenticated) {
        this.router.navigate(['/login']);
        return;
      }
      if (this.tour) {
        this.reviewService
          .createReview({ 
            tour: this.tour.id, 
            rating: this.rating, 
            comment: this.comment })
          .subscribe({
            next: () => {
              alert('Review submitted successfully!');
              this.tourService.getTourById(this.tour!.id).subscribe((updatedTour) => {
                this.tour = updatedTour;
                this.rating = 1;
                this.comment = '';
              });
            },
            error: (err) => {
              alert('Failed to submit review');
            },
          });
      }
    });
  }
}