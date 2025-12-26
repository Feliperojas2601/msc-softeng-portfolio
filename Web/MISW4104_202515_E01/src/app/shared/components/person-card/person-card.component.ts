import { Component, inject, input, output, signal } from '@angular/core';
import { Actor } from '../../../actor/interfaces/actor.interface';
import { MovieCardComponent } from '../movie-card/movie-card.component';
import { Director } from '../../../director/interfaces/director.interface';
import { Router } from '@angular/router';

@Component({
    selector: 'app-person-card',
    templateUrl: './person-card.component.html',
    styleUrls: ['./person-card.component.css'],
    imports: [MovieCardComponent],
})
export class PersonCardComponent {
    person = input.required<Actor | Director>();
    showDetailEvent = output<boolean>();

    private readonly router = inject(Router);

    showMovies = signal(false);

    toggleMovies() {
        this.showMovies.update((value) => !value);
    }

    showPersonDetail() {
        this.showDetailEvent.emit(true);
    }

    goToMovie(movieId: string): void {
        this.router.navigate(['/movie', movieId]);
    }
}
