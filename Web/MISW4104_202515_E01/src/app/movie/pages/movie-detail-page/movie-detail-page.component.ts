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
import { Movie } from '../../interfaces/movie.interface';
import { MovieService } from '../../services/movie.service';
import { ActivatedRoute, Router } from '@angular/router';
import {
    FormBuilder,
    FormGroup,
    Validators,
    ReactiveFormsModule,
} from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { InputFieldComponent } from '../../../shared/components/input-field/input-field.component';
import {
    AssociationModalComponent,
    AssociationItem,
} from '../../../shared/components/association-modal/association-modal.component';
import { ActorService } from '../../../actor/services/actor.service';
import { Actor } from '../../../actor/interfaces/actor.interface';

@Component({
    selector: 'app-movie-detail-page',
    imports: [
        CommonModule,
        ReactiveFormsModule,
        InputFieldComponent,
        AssociationModalComponent,
    ],
    templateUrl: './movie-detail-page.component.html',
    styleUrls: ['./movie-detail-page.component.css'],
})
export class MovieDetailPageComponent implements OnInit {
    public readonly movieDetails = signal<Movie | null>(null);
    public readonly movieService = inject(MovieService);
    public readonly actorService = inject(ActorService);
    public readonly isSubmitting = signal<boolean>(false);
    public readonly showReviewForm = signal<boolean>(false);

    public showActorModal = signal<boolean>(false);
    public availableActors = signal<AssociationItem[]>([]);

    @ViewChild(AssociationModalComponent)
    actorModal!: AssociationModalComponent;

    private readonly route = inject(ActivatedRoute);
    private readonly router = inject(Router);
    private readonly fb = inject(FormBuilder);
    private readonly toastr = inject(ToastrService);

    reviewForm: FormGroup = this.fb.group({
        text: ['', [Validators.required]],
        score: [5, [Validators.required, Validators.min(1), Validators.max(5)]],
        creator: ['', [Validators.required]],
    });

    ngOnInit(): void {
        const movieId = this.route.snapshot.paramMap.get('id');
        this.getMovieById(movieId);
    }

    get stars(): number[] {
        return new Array(5).fill(0).map((_, i) => i);
    }

    isStarFilled(index: number): boolean {
        const movie = this.movieDetails();
        if (!movie) return false;
        return index < Math.floor(movie.popularity);
    }

    isStarHalf(index: number): boolean {
        const movie = this.movieDetails();
        if (!movie) return false;
        const decimal = movie.popularity - Math.floor(movie.popularity);
        return index === Math.floor(movie.popularity) && decimal >= 0.5;
    }

    getReviewStars(score: number): number[] {
        return new Array(5).fill(0).map((_, i) => i + 1);
    }

    getError(fieldName: string): string | null {
        const field = this.reviewForm.get(fieldName);
        if (field?.invalid && (field?.dirty || field?.touched)) {
            if (field?.errors?.['required']) {
                return 'Este campo es requerido';
            }
            if (field?.errors?.['min']) {
                return 'La puntuación mínima es 1';
            }
            if (field?.errors?.['max']) {
                return 'La puntuación máxima es 5';
            }
        }
        return null;
    }

    toggleReviewForm(): void {
        this.showReviewForm.update((value) => !value);
        if (!this.showReviewForm()) {
            this.reviewForm.reset({ score: 5 });
        }
    }

    onSubmitReview(): void {
        if (this.reviewForm.invalid) {
            Object.keys(this.reviewForm.controls).forEach((key) => {
                this.reviewForm.get(key)?.markAsTouched();
            });
            return;
        }

        const movie = this.movieDetails();
        if (!movie) return;

        this.isSubmitting.set(true);
        const reviewData = {
            text: this.reviewForm.value.text,
            score: Number(this.reviewForm.value.score),
            creator: this.reviewForm.value.creator,
        };

        this.movieService.createReview(movie.id, reviewData).subscribe({
            next: (review) => {
                console.log('Reseña creada:', review);
                this.toastr.success(
                    'Tu reseña ha sido publicada exitosamente',
                    'Reseña creada',
                    { closeButton: true },
                );
                this.isSubmitting.set(false);
                this.reviewForm.reset({ score: 5 });
                this.showReviewForm.set(false);
                // Recargar los detalles de la película para mostrar la nueva reseña
                this.getMovieById(movie.id);
            },
            error: (error) => {
                console.error('Error creando reseña:', error);
                this.isSubmitting.set(false);
            },
        });
    }

    private getMovieById(movieId: string | null): void {
        if (!movieId) return;
        this.movieService.getMovieById(movieId).subscribe({
            next: (movieResponse) => {
                this.movieDetails.set(movieResponse);
            },
            error: (error) => {
                console.error('Error fetching movie details:', error);
            },
        });
    }

    goToActor(actorId: string): void {
        this.router.navigate(['/actor', actorId]);
    }

    goToDirector(directorId: string): void {
        this.router.navigate(['/director', directorId]);
    }

    openAddActorModal(): void {
        this.loadAvailableActors();
        this.showActorModal.set(true);
    }

    closeActorModal(): void {
        this.showActorModal.set(false);
    }

    private loadAvailableActors(): void {
        this.actorService.getActors().subscribe({
            next: (actors: Actor[]) => {
                const movieActorIds =
                    this.movieDetails()?.actors.map((a) => a.id) || [];
                const available = actors
                    .filter((actor) => !movieActorIds.includes(actor.id))
                    .map((actor) => ({
                        id: actor.id,
                        name: actor.name,
                        photo: actor.photo,
                    }));
                this.availableActors.set(available);
            },
            error: (error) => {
                console.error('Error loading actors:', error);
            },
        });
    }

    onActorSelected(actorId: string): void {
        const movieId = this.movieDetails()?.id;
        if (!movieId) return;

        this.movieService.addActorToMovie(movieId, actorId).subscribe({
            next: () => {
                console.log('Actor added successfully');
                this.actorModal.handleSuccess();
                this.getMovieById(movieId);
            },
            error: (error) => {
                console.error('Error adding actor to movie:', error);
                this.actorModal.handleError();
            },
        });
    }
}
