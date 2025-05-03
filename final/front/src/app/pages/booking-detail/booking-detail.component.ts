import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookingService } from '../../services/booking.service';
import { AuthService } from '../../services/auth.service';
import { Booking } from '../../models/booking.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-booking-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './booking-detail.component.html',
})
export class BookingDetailComponent {
  booking: Booking | null = null;
  loading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private bookingService: BookingService,
    private authService: AuthService
  ) {
    this.authService.isAuthenticated().subscribe((isAuthenticated) => {
      if (!isAuthenticated) {
        this.router.navigate(['/login']);
        return;
      }
      const bookingId = this.route.snapshot.paramMap.get('id');
      if (bookingId) {
        this.bookingService.getBookingById(bookingId).subscribe({
          next: (booking) => {
            this.booking = booking;
            this.loading = false;
          },
          error: (err) => {
            console.error('Failed to fetch booking:', err);
            this.loading = false;
          },
        });
      }
    });
  }

  updateStatus(status: string): void {
    if (this.booking) {
      this.bookingService.updateBooking(this.booking.id, { status }).subscribe({
        next: (updatedBooking) => {
          this.booking = updatedBooking;
        },
        error: (err) => {
          alert('Failed to update booking');
        },
      });
    }
  }
}