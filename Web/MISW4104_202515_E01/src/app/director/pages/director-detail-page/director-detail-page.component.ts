import {
    Component,
    effect,
    inject,
    input,
    OnInit,
    signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Director } from '../../interfaces/director.interface';
import { DirectorService } from '../../services/director.service';
import { MovieCardComponent } from '../../../shared/components/movie-card/movie-card.component';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
    selector: 'app-director-detail-page',
    imports: [CommonModule, MovieCardComponent],
    templateUrl: './director-detail-page.component.html',
    styleUrls: ['./director-detail-page.component.css'],
})
export class DirectorDetailPageComponent implements OnInit {
    public readonly directorDetails = signal<Director | null>(null);
    public readonly directorService = inject(DirectorService);

    private readonly router = inject(Router);
    private readonly route = inject(ActivatedRoute);

    ngOnInit(): void {
        const directorId = this.route.snapshot.paramMap.get('id');
        this.getDirectorById(directorId);
    }

    private getDirectorById(directorId: string | null): void {
        if (!directorId) return;
        this.directorService.getDirectorById(directorId).subscribe({
            next: (directorResponse) => {
                this.directorDetails.set(directorResponse);
            },
            error: (error) => {
                console.error('Error fetching director details:', error);
            },
        });
    }

    goToMovie(movieId: string): void {
        this.router.navigate(['/movie', movieId]);
    }
}
