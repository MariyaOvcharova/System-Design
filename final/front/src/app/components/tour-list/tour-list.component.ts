import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TourService } from '../../services/tour.service';
import { Tour } from '../../models/tour.model';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-tour-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './tour-list.component.html',
})
export class TourListComponent {
  @Input() tours: Tour[] = [];
  @Output() filterChange = new EventEmitter<Tour[]>();
  loading: boolean = true;
  selectedStars: number[] = [];
  priceRange: number = 0;
  maxPrice: number = 0;
  filteredTours: Tour[] = [];

  filters = {
    stars: 0,
    category_id: '',
    min_price: 0,
    max_price: Infinity,
    start_date: ''
  };

  constructor(private tourService: TourService, private router: Router) {}

  ngOnChanges(): void {
    this.loading = false;
    this.updateMaxPrice();
    this.filters.max_price = this.maxPrice;
    this.filteredTours = [...this.tours];
    this.applyFilters();
  }
  
  

  getAverageRating(tour: Tour): { display: string; stars: number } {
    if (!tour.reviews?.length) {
      return { display: 'Нет отзывов', stars: 0 };
    }
    const average = tour.reviews.reduce((sum, r) => sum + r.rating, 0) / tour.reviews.length;
    const stars = Math.floor(average);
    return { display: average.toFixed(1), stars };
  }

  formatPrice(price: string): string {
    return parseFloat(price).toFixed(0);
  }

  updateMaxPrice(): void {
    if (this.tours.length) {
      this.maxPrice = Math.max(...this.tours.map((tour) => parseFloat(tour.price)));
    }
  }

  applyFilters(): void {
    this.filteredTours = this.tours.filter(tour => {
      const avgRating = this.getAverageRating(tour).stars;
  
      const matchesStars = this.filters.stars ? avgRating >= +this.filters.stars : true;
      const matchesCategory = this.filters.category_id ? tour.category?.id === this.filters.category_id : true;
  
      const price = parseFloat(tour.price);
      const matchesPrice =
        (!this.filters.min_price || price >= +this.filters.min_price) &&
        (!this.filters.max_price || price <= +this.filters.max_price);
  
      const matchesDate = this.filters.start_date
        ? new Date(tour.start_date) >= new Date(this.filters.start_date)
        : true;
  
      return matchesStars && matchesCategory && matchesPrice && matchesDate;
    });
  }
  

  viewTour(tourId: string): void {
    this.router.navigate(['/tour', tourId]);
  }
}