import { Component, inject, OnInit, signal } from '@angular/core';
import { DirectorService } from '../../services/director.service';
import { Director } from '../../interfaces/director.interface';
import { LoaderComponent } from '../../../shared/components/loader/loader.component';
import { PersonCardComponent } from '../../../shared/components/person-card/person-card.component';
import { Router } from '@angular/router';

@Component({
    selector: 'app-director-list-page',
    templateUrl: './director-list-page.component.html',
    styleUrls: ['./director-list-page.component.css'],
    imports: [PersonCardComponent, LoaderComponent],
})
export class DirectorListPageComponent implements OnInit {
    private readonly directorService = inject(DirectorService);
    private readonly router = inject(Router);

    public readonly directors = signal<Director[]>([]);
    public readonly isLoading = signal<boolean>(false);
    public readonly searchQuery = signal<string>('');

    getDirectors(): void {
        if (this.isLoading()) return;
        this.isLoading.set(true);
        this.directorService.getDirectors().subscribe({
            // next es el callback que se ejecuta cuando se recibe la respuesta
            // error es el callback que se ejecuta cuando ocurre un error
            // complete es el callback que se ejecuta cuando se completa la respuesta
            next: (directorsResponse) => {
                this.directors.set(directorsResponse);
                this.isLoading.set(false);
            },
            error: (error) => {
                console.error('Error fetching directors:', error);
                this.isLoading.set(false);
            },
            complete: () => {
                this.isLoading.set(false);
            },
        });
    }

    ngOnInit() {
        this.getDirectors();
    }

    onSearch(query: string): void {
        this.searchQuery.set(query);
        this.filterDirectors();
    }

    private filterDirectors(): void {
        const query = this.searchQuery();
        if (!query) {
            this.getDirectors();
            return;
        }
        this.directors.set(
            this.directors().filter((director) =>
                director.name.toLowerCase().includes(query.toLowerCase()),
            ),
        );
    }

    showDetailDirector(directorId: string): void {
        this.router.navigate(['/director', directorId]);
    }
}
