import { Component, input, output, signal } from '@angular/core';
import { MovieCard } from '../../interfaces/movie.interface';
import { Movie } from '../../../movie/interfaces/movie.interface';
import { DatePipe } from '@angular/common';

@Component({
    selector: 'app-movie-card',
    templateUrl: './movie-card.component.html',
    styleUrls: ['./movie-card.component.css'],
    imports: [DatePipe],
})
export class MovieCardComponent {
    movie = input.required<MovieCard | Movie>();
    showDetails = input<boolean>(false);
    smallSize = input<boolean>(false);
    isHovered = signal<boolean>(false);
    showDetailEvent = output<boolean>();

    get stars(): number[] {
        return new Array(5).fill(0).map((_, i) => i);
    }

    isStarFilled(index: number): boolean {
        return index < Math.floor(this.movie().popularity);
    }

    isStarHalf(index: number): boolean {
        const decimal =
            this.movie().popularity - Math.floor(this.movie().popularity);
        return index === Math.floor(this.movie().popularity) && decimal >= 0.5;
    }

    onMouseEnter(): void {
        this.isHovered.set(true);
    }

    onMouseLeave(): void {
        this.isHovered.set(false);
    }

    isFullMovie(movie: MovieCard | Movie): movie is Movie {
        return 'genre' in movie;
    }

    get fullMovie(): (Movie & { sampleActors: string }) | null {
        const m = this.movie();
        if (this.isFullMovie(m)) {
            return {
                ...m,
                sampleActors: m.actors.map((actor) => actor.name).join(', '),
            };
        }
        return null;
    }

    showMovieDetail() {
        this.showDetailEvent.emit(true);
    }
}
