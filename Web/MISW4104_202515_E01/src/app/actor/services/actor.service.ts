import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { Observable } from 'rxjs';
import { Actor } from '../interfaces/actor.interface';

@Injectable({
    providedIn: 'root',
})
export class ActorService {
    private readonly http = inject(HttpClient);
    private readonly baseUrl = environment.apiUrl + '/actors';

    getActors(): Observable<Actor[]> {
        return this.http.get<Actor[]>(this.baseUrl);
    }

    getActorById(id: string): Observable<Actor> {
        return this.http.get<Actor>(`${this.baseUrl}/${id}`);
    }

    createActor(actor: Omit<Actor, 'id'>): Observable<Actor> {
        return this.http.post<Actor>(this.baseUrl, actor);
    }

    addMovieToActor(actorId: string, movieId: string): Observable<void> {
        return this.http.post<void>(
            `${this.baseUrl}/${actorId}/movies/${movieId}`,
            {},
        );
    }
}
