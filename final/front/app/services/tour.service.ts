import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Tour, TourFilter } from '../models/tour.model';

@Injectable({
  providedIn: 'root',
})
export class TourService {
  private apiUrl = 'http://127.0.0.1:8008/api/tours';

  constructor(private http: HttpClient) {}

  getTours(filters: TourFilter = {}): Observable<Tour[]> {
    let params = new HttpParams();
    if (filters.category_id) params = params.set('category_id', filters.category_id);
    if (filters.min_price !== undefined) params = params.set('min_price', filters.min_price.toString());
    if (filters.max_price !== undefined) params = params.set('max_price', filters.max_price.toString());
    if (filters.start_date) params = params.set('start_date', filters.start_date);
    return this.http.get<Tour[]>(`${this.apiUrl}/`, { params });
  }  

  getTourById(tourId: string): Observable<Tour> {
    return this.http.get<Tour>(`${this.apiUrl}/${tourId}/`);
  }
}