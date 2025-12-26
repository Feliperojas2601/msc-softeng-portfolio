import { Component, inject, OnInit, signal } from '@angular/core';
import { ActorService } from '../../services/actor.service';
import { Actor } from '../../interfaces/actor.interface';
import { PersonCardComponent } from '../../../shared/components/person-card/person-card.component';
import { LoaderComponent } from '../../../shared/components/loader/loader.component';
import { Router } from '@angular/router';

@Component({
    selector: 'app-actor-list-page',
    templateUrl: './actor-list-page.component.html',
    styleUrls: ['./actor-list-page.component.css'],
    imports: [PersonCardComponent, LoaderComponent],
})
export class ActorListPageComponent implements OnInit {
    private readonly actorService = inject(ActorService);
    private readonly router = inject(Router);

    public readonly actors = signal<Actor[]>([]);
    public readonly isLoading = signal<boolean>(false);
    public readonly searchQuery = signal<string>('');

    getActors(): void {
        if (this.isLoading()) return;
        this.isLoading.set(true);
        this.actorService.getActors().subscribe({
            // next es el callback que se ejecuta cuando se recibe la respuesta
            // error es el callback que se ejecuta cuando ocurre un error
            // complete es el callback que se ejecuta cuando se completa la respuesta
            next: (actorsResponse) => {
                this.actors.set(actorsResponse);
                this.isLoading.set(false);
            },
            error: (error) => {
                console.error('Error fetching actors:', error);
                this.isLoading.set(false);
            },
            complete: () => {
                this.isLoading.set(false);
            },
        });
    }

    ngOnInit() {
        this.getActors();
    }

    onSearch(query: string): void {
        this.searchQuery.set(query);
        this.filterActors();
    }

    private filterActors(): void {
        const query = this.searchQuery();
        if (!query) {
            this.getActors();
            return;
        }
        this.actors.set(
            this.actors().filter((actor) =>
                actor.name.toLowerCase().includes(query.toLowerCase()),
            ),
        );
    }

    showDetailActor(actorId: string): void {
        this.router.navigate(['/actor', actorId]);
    }
}
