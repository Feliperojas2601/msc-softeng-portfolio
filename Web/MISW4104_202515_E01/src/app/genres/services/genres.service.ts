import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { Genre } from '../interfaces/genre.interface';

@Injectable({
    providedIn: 'root',
})
export class GenresService {
    private readonly http = inject(HttpClient);
    private readonly baseUrl = environment.apiUrl + '/genres';

    getGenres(): Observable<Genre[]> {
        return this.http.get<Genre[]>(this.baseUrl);
    }

    createGenre(genre: { type: string }): Observable<Genre> {
        return this.http.post<Genre>(this.baseUrl, genre);
    }
}
