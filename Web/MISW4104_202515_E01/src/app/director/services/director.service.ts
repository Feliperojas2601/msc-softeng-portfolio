import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { Observable } from 'rxjs';
import { Director } from '../interfaces/director.interface';

@Injectable({
    providedIn: 'root',
})
export class DirectorService {
    private readonly http = inject(HttpClient);
    private readonly baseUrl = environment.apiUrl + '/directors';

    getDirectors(): Observable<Director[]> {
        return this.http.get<Director[]>(this.baseUrl);
    }

    getDirectorById(id: string): Observable<Director> {
        return this.http.get<Director>(`${this.baseUrl}/${id}`);
    }

    createDirector(
        director: Omit<Director, 'id' | 'movies'>,
    ): Observable<Director> {
        return this.http.post<Director>(this.baseUrl, director);
    }
}
