import {
    Component,
    effect,
    inject,
    input,
    OnInit,
    signal,
    ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Actor } from '../../interfaces/actor.interface';
import { ActorService } from '../../services/actor.service';
import { MovieCardComponent } from '../../../shared/components/movie-card/movie-card.component';
import { ActivatedRoute, Router } from '@angular/router';
import {
    AssociationModalComponent,
    AssociationItem,
} from '../../../shared/components/association-modal/association-modal.component';
import { MovieService } from '../../../movie/services/movie.service';
import { Movie } from '../../../movie/interfaces/movie.interface';

@Component({
    selector: 'app-actor-detail-page',
    imports: [CommonModule, MovieCardComponent, AssociationModalComponent],
    templateUrl: './actor-detail-page.component.html',
    styleUrls: ['./actor-detail-page.component.css'],
})
export class ActorDetailPageComponent implements OnInit {
    public readonly actorDetails = signal<Actor | null>(null);
    public readonly actorService = inject(ActorService);
    public readonly movieService = inject(MovieService);

    private readonly router = inject(Router);
    private readonly route = inject(ActivatedRoute);

    public showMovieModal = signal<boolean>(false);
    public availableMovies = signal<AssociationItem[]>([]);

    @ViewChild(AssociationModalComponent)
    movieModal!: AssociationModalComponent;

    ngOnInit(): void {
        const actorId = this.route.snapshot.paramMap.get('id');
        this.getActorById(actorId);
    }

    private getActorById(actorId: string | null): void {
        if (!actorId) return;
        this.actorService.getActorById(actorId).subscribe({
            next: (actorResponse) => {
                this.actorDetails.set(actorResponse);
            },
            error: (error) => {
                console.error('Error fetching actor details:', error);
            },
        });
    }

    goToMovie(movieId: string): void {
        this.router.navigate(['/movie', movieId]);
    }

    openAddMovieModal(): void {
        this.loadAvailableMovies();
        this.showMovieModal.set(true);
    }

    closeMovieModal(): void {
        this.showMovieModal.set(false);
    }

    private loadAvailableMovies(): void {
        this.movieService.getMovies().subscribe({
            next: (movies: Movie[]) => {
                // Filter out movies that are already associated with the actor
                const actorMovieIds =
                    this.actorDetails()?.movies.map((m) => m.id) || [];
                const available = movies
                    .filter((movie) => !actorMovieIds.includes(movie.id))
                    .map((movie) => ({
                        id: movie.id,
                        name: movie.title,
                        photo: movie.poster,
                    }));
                this.availableMovies.set(available);
            },
            error: (error) => {
                console.error('Error loading movies:', error);
            },
        });
    }

    onMovieSelected(movieId: string): void {
        const actorId = this.actorDetails()?.id;
        if (!actorId) return;

        this.actorService.addMovieToActor(actorId, movieId).subscribe({
            next: () => {
                console.log('Movie added successfully');
                this.movieModal.handleSuccess();
                // Reload actor details to show the new movie
                this.getActorById(actorId);
            },
            error: (error) => {
                console.error('Error adding movie to actor:', error);
                this.movieModal.handleError();
            },
        });
    }
}
