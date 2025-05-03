export interface Tour {
    id: string;
    name: string;
    description: string;
    price: string;
    start_date: string;
    end_date: string;
    rating: number;
    category: { id: string; name: string; description: string };
    is_active: boolean;
    reviews: Review[];
    photo_urls: string[];
  }
  
  export interface Review {
    id: string;
    user: string;
    tour: string;
    rating: number;
    comment: string;
    created_at: string;
  }

  export interface TourFilter {
    category_id?: string;
    min_price?: number;
    max_price?: number;
    start_date?: string;
  }
