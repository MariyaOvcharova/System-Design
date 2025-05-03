import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Booking } from '../models/booking.model';

@Injectable({
  providedIn: 'root',
})
export class BookingService {
  private apiUrl = 'http://127.0.0.1:8008/api/bookings';

  constructor(private http: HttpClient) {}

  getBookings(): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.apiUrl}/`);
  }

  getBookingById(bookingId: string): Observable<Booking> {
    return this.http.get<Booking>(`${this.apiUrl}/${bookingId}/`);
  }

  createBooking(bookingData: { tour_id: string }): Observable<Booking> {
    return this.http.post<Booking>(`${this.apiUrl}/`, bookingData);
  }

  updateBooking(bookingId: string, bookingData: { status: string }): Observable<Booking> {
    return this.http.put<Booking>(`${this.apiUrl}/${bookingId}/`, bookingData);
  }

  deleteBooking(bookingId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${bookingId}/`);
  }
}