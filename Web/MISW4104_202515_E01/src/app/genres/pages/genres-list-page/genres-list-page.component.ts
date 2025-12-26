import { Genre } from '../../interfaces/genre.interface';
import { GenresService } from '../../services/genres.service';
import { Component, OnInit, inject, signal } from '@angular/core';
import { LoaderComponent } from '../../../shared/components/loader/loader.component';
import { genreDescriptions } from '../../../shared/utils/contants';
import { MovieCardComponent } from '../../../shared/components/movie-card/movie-card.component';
import { Router } from '@angular/router';

@Component({
    selector: 'app-genres-list-page',
    templateUrl: './genres-list-page.component.html',
    styleUrls: ['./genres-list-page.component.css'],
    imports: [LoaderComponent, MovieCardComponent],
})
export class GenresListPageComponent implements OnInit {
    public readonly genreService = inject(GenresService);
    public readonly genres = signal<Genre[]>([]);
    public readonly isLoading = signal<boolean>(false);
    public readonly expandedGenres = signal<Set<string>>(new Set());

    private readonly router = inject(Router);

    getGenres(): void {
        if (this.isLoading()) return;
        this.isLoading.set(true);
        this.genreService.getGenres().subscribe({
            next: (genresResponse) => {
                this.genres.set(genresResponse);
                this.isLoading.set(false);
            },
            error: (error) => {
                console.error('Error fetching genres:', error);
                this.isLoading.set(false);
            },
            complete: () => {
                this.isLoading.set(false);
            },
        });
    }

    getGenreDescription(genreType: string): string {
        return genreDescriptions[genreType] || 'No description available.';
    }

    toggleGenre(genreId: string): void {
        const expanded = this.expandedGenres();
        if (expanded.has(genreId)) {
            expanded.delete(genreId);
        } else {
            expanded.add(genreId);
        }
        this.expandedGenres.set(new Set(expanded));
    }

    isGenreExpanded(genreId: string): boolean {
        return this.expandedGenres().has(genreId);
    }

    ngOnInit() {
        this.getGenres();
    }

    goToMovie(movieId: string): void {
        this.router.navigate(['/movie', movieId]);
    }
}
