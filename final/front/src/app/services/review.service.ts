import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Review } from '../models/tour.model';

@Injectable({
  providedIn: 'root',
})
export class ReviewService {
  private apiUrl = 'http://127.0.0.1:8008/api/reviews';

  constructor(private http: HttpClient) {}

  createReview(reviewData: { tour: string; rating: number; comment: string }): Observable<Review> {
    return this.http.post<Review>(`${this.apiUrl}/`, reviewData);
  }
}