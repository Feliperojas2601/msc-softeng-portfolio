import {
    ChangeDetectionStrategy,
    Component,
    computed,
    inject,
    OnInit,
    signal,
} from '@angular/core';
import { MovieCardComponent } from '../../../shared/components/movie-card/movie-card.component';
import { LoaderComponent } from '../../../shared/components/loader/loader.component';
import { MovieService } from '../../../movie/services/movie.service';
import { Router } from '@angular/router';
import { Movie } from '../../../movie/interfaces/movie.interface';

@Component({
    selector: 'app-home-page',
    imports: [MovieCardComponent, LoaderComponent],
    templateUrl: './home-page.component.html',
    styleUrls: ['./home-page.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomePageComponent implements OnInit {
    private readonly movieService = inject(MovieService);
    private readonly router = inject(Router);

    public readonly popularMovies = signal<Movie[]>([]);
    public readonly isLoading = signal<boolean>(false);
    public readonly currentIndex = signal<number>(0);
    public readonly slideWidth = 25;
    public readonly slidesToShow = 4;

    public readonly maxIndex = computed(() => {
        const total = this.popularMovies().length;
        return Math.max(0, total - this.slidesToShow);
    });

    ngOnInit(): void {
        this.getPopularMovies();
    }

    getPopularMovies(): void {
        if (this.isLoading()) return;
        this.isLoading.set(true);
        this.movieService.getMovies().subscribe({
            next: (moviesResponse) => {
                const sorted = [...moviesResponse]
                    .sort((a, b) => b.popularity - a.popularity)
                    .slice(0, 12);
                this.popularMovies.set(sorted);
                this.isLoading.set(false);
            },
            error: (error) => {
                console.error('Error fetching popular movies:', error);
                this.isLoading.set(false);
            },
        });
    }

    nextSlide(): void {
        const current = this.currentIndex();
        const max = this.maxIndex();
        if (current < max) {
            this.currentIndex.set(current + 1);
        }
    }

    previousSlide(): void {
        const current = this.currentIndex();
        if (current > 0) {
            this.currentIndex.set(current - 1);
        }
    }

    showDetailMovie(movie: Movie): void {
        this.router.navigate(['/movie', movie.id]);
    }
}
