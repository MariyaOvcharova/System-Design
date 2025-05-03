import { Component } from '@angular/core';
import { TourListComponent } from '../../components/tour-list/tour-list.component';
import { TourService } from '../../services/tour.service';
import { Tour } from '../../models/tour.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Category } from '../../models/category.model';
import { CategoryService } from '../../services/category.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, TourListComponent],
  templateUrl: './home.component.html',
})
export class HomeComponent {
  tours: Tour[] = [];
  filteredTours: Tour[] = [];
  categories: Category[] = [];

  filters = {
    category_id: '',
    min_price: 0,
    max_price: 10000000,
    start_date: '',
    stars: [] as number[],
  };

  constructor(
    private tourService: TourService,
    private categoryService: CategoryService
  ) {}

  ngOnInit(): void {
    this.fetchCategories();
    this.fetchTours();
  }

  fetchCategories(): void {
    this.categoryService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (err) => {
        console.error('Failed to fetch categories:', err);
      },
    });
  }

  onStarChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    const star = Number(input.value);
    if (input.checked) {
      this.filters.stars.push(star);
    } else {
      this.filters.stars = this.filters.stars.filter(s => s !== star);
    }
    this.applyFilters();
  }
  

  applyFilters(): void {
    const { stars, ...apiFilters } = this.filters;
    this.tourService.getTours(apiFilters).subscribe({
      next: (tours) => {
        this.tours = tours;
        this.filteredTours = tours.filter((tour) => {
          const avgRating = tour.reviews?.length
            ? tour.reviews.reduce((sum, r) => sum + r.rating, 0) / tour.reviews.length
            : 0;
          
          const matchesCategory = this.filters.category_id
            ? tour.category.id === this.filters.category_id
            : true;
          
          return matchesCategory && (this.filters.stars.length
            ? this.filters.stars.some(star => avgRating >= star)
            : true);
        });
      },
      error: (err) => {
        console.error('Failed to fetch tours:', err);
      },
    });
  }
  
  resetFilters(): void {
    this.filters = {
      category_id: '',
      min_price: 0,
      max_price: 10000000,
      start_date: '',
      stars: []
    };
    this.applyFilters();
  }
  

  fetchTours(): void {
    this.applyFilters();
  }
}