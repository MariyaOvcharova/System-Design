import { Tour } from './tour.model';

export interface Booking {
  id: string;
  user: string;
  tour: Tour;
  tour_id: string;
  booking_date: string;
  status: string;
}