import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { BookingService } from '../../services/booking.service';
import { AuthService } from '../../services/auth.service';
import { Booking } from '../../models/booking.model';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-bookings',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './bookings.component.html',
})
export class BookingsComponent {
  bookings: Booking[] = [];
  loading: boolean = true;

  constructor(
    private bookingService: BookingService,
    private authService: AuthService,
    private router: Router
  ) {
    this.authService.isAuthenticated().subscribe((isAuthenticated) => {
      if (!isAuthenticated) {
        this.router.navigate(['/login']);
        return;
      }
      this.bookingService.getBookings().subscribe({
        next: (bookings) => {
          this.bookings = bookings;
          this.loading = false;
        },
        error: (err) => {
          console.error('Failed to fetch bookings:', err);
          this.loading = false;
        },
      });
    });
  }

  deleteBooking(bookingId: string): void {
    if (confirm('Are you sure you want to delete this booking?')) {
      this.bookingService.deleteBooking(bookingId).subscribe({
        next: () => {
          this.bookings = this.bookings.filter((booking) => booking.id !== bookingId);
        },
        error: (err) => {
          alert('Failed to delete booking');
        },
      });
    }
  }
}