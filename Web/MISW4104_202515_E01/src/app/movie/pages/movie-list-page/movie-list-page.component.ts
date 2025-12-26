import { Component, inject, OnInit, signal } from '@angular/core';
import { MovieCardComponent } from '../../../shared/components/movie-card/movie-card.component';
import { Movie } from '../../interfaces/movie.interface';
import { MovieService } from '../../services/movie.service';
import { LoaderComponent } from '../../../shared/components/loader/loader.component';
import { Router } from '@angular/router';

@Component({
    selector: 'app-movie-list-page',
    templateUrl: './movie-list-page.component.html',
    styleUrls: ['./movie-list-page.component.css'],
    imports: [MovieCardComponent, LoaderComponent],
})
export class MovieListPageComponent implements OnInit {
    private readonly movieService = inject(MovieService);
    private readonly router = inject(Router);

    public readonly movies = signal<Movie[]>([]);
    public readonly cachedMovies = signal<Movie[]>([]);
    public readonly isLoading = signal<boolean>(false);
    public readonly searchQuery = signal<string>('');
    public readonly genres = signal<string[]>([]);
    public readonly showDropdown = signal<boolean>(false);
    public readonly selectedGenre = signal<string>('Todos');

    getMovies(): void {
        if (this.isLoading()) return;
        this.isLoading.set(true);
        this.movieService.getMovies().subscribe({
            next: (moviesResponse) => {
                this.movies.set(moviesResponse);
                this.cachedMovies.set(moviesResponse);
                this.processGenres(moviesResponse);
                this.isLoading.set(false);
            },
            error: (error) => {
                console.error('Error fetching movies:', error);
                this.isLoading.set(false);
            },
            complete: () => {
                this.isLoading.set(false);
            },
        });
    }

    processGenres(movies: Movie[]): void {
        const genres = new Set<string>();
        genres.add('Todos');
        for (const movie of movies) {
            genres.add(movie.genre.type);
        }
        this.genres.set(Array.from(genres));
    }

    ngOnInit() {
        this.getMovies();
    }

    onSearch(query: string): void {
        this.searchQuery.set(query);
        this.filterMovies();
    }

    private filterMovies(): void {
        const query = this.searchQuery();
        if (!query) {
            this.getMovies();
            return;
        }
        this.movies.set(
            this.movies().filter((movie) =>
                movie.title.toLowerCase().includes(query.toLowerCase()),
            ),
        );
    }

    onFilterByGenre(genre: string): void {
        this.selectedGenre.set(genre);
        this.showDropdown.set(false);
        if (genre === 'Todos') {
            this.movies.set(this.cachedMovies());
        } else {
            this.movies.set(
                this.cachedMovies().filter(
                    (movie) => movie.genre.type === genre,
                ),
            );
        }
    }

    toggleDropdown(): void {
        this.showDropdown.update((value) => !value);
    }

    showDetailMovie(movie: Movie): void {
        this.router.navigate(['/movie', movie.id]);
    }
}
