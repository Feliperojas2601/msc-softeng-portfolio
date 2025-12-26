import { inject, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie, Review } from '../interfaces/movie.interface';

@Injectable({
    providedIn: 'root',
})
export class MovieService {
    private readonly baseUrl = environment.apiUrl + '/movies';
    private readonly http = inject(HttpClient);

    getMovies(): Observable<Movie[]> {
        return this.http.get<Movie[]>(this.baseUrl);
    }

    getMovieById(id: string): Observable<Movie> {
        return this.http.get<Movie>(`${this.baseUrl}/${id}`);
    }

    createReview(
        movieId: string,
        review: Omit<Review, 'id'>,
    ): Observable<Review> {
        return this.http.post<Review>(
            `${this.baseUrl}/${movieId}/reviews`,
            review,
        );
    }

    addActorToMovie(movieId: string, actorId: string): Observable<void> {
        return this.http.post<void>(
            `${this.baseUrl}/${movieId}/actors/${actorId}`,
            {},
        );
    }
}
