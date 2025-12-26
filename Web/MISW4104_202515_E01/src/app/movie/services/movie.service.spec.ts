import { TestBed } from '@angular/core/testing';
import { MovieService } from './movie.service';
import { provideHttpClient } from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';
import { environment } from '../../../environments/environment.development';
import { fa, faker } from '@faker-js/faker';
import { Movie } from '../interfaces/movie.interface';

describe('MovieService', () => {
    let service: MovieService;
    let httpMock: HttpTestingController;
    const baseUrl = environment.apiUrl + '/movies';
    const mockMovies: Movie[] = Array.from({ length: 3 }, () => ({
        id: faker.string.uuid(),
        title: faker.lorem.words(3),
        poster: faker.image.url(),
        duration: faker.number.int({ min: 90, max: 180 }),
        country: faker.location.country(),
        releaseDate: faker.date.past().toISOString(),
        popularity: faker.number.float({ min: 1, max: 5 }),
        director: {
            id: faker.string.uuid(),
            name: faker.person.fullName(),
            photo: faker.image.avatar(),
            nationality: faker.location.country(),
            birthDate: faker.date.past().toISOString(),
            biography: faker.lorem.paragraph(),
        },
        actors: [],
        genre: {
            id: faker.string.uuid(),
            type: faker.music.genre(),
        },
        platforms: [],
        reviews: [],
        youtubeTrailer: {
            id: faker.string.uuid(),
            name: faker.lorem.words(2),
            url: faker.internet.url(),
            duration: faker.number.int({ min: 60, max: 600 }),
            channel: faker.internet.domainWord(),
        },
    }));
    const mockMovie: Movie = {
        id: '1',
        title: faker.lorem.words(3),
        poster: faker.image.url(),
        duration: faker.number.int({ min: 90, max: 180 }),
        country: faker.location.country(),
        releaseDate: faker.date.past().toISOString(),
        popularity: faker.number.float({ min: 1, max: 5 }),
        director: {
            id: faker.string.uuid(),
            name: faker.person.fullName(),
            photo: faker.image.avatar(),
            nationality: faker.location.country(),
            birthDate: faker.date.past().toISOString(),
            biography: faker.lorem.paragraph(),
        },
        actors: [],
        genre: {
            id: faker.string.uuid(),
            type: faker.music.genre(),
        },
        platforms: [],
        reviews: [],
        youtubeTrailer: {
            id: faker.string.uuid(),
            name: faker.lorem.words(2),
            url: faker.internet.url(),
            duration: faker.number.int({ min: 60, max: 600 }),
            channel: faker.internet.domainWord(),
        },
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [provideHttpClient(), provideHttpClientTesting()],
        });
        service = TestBed.inject(MovieService);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should fetch movies successfully', () => {
        service.getMovies().subscribe((movies) => {
            expect(movies).toBeDefined();
            expect(movies.length).toBe(3);
            expect(movies).toEqual(mockMovies);
        });
        const req = httpMock.expectOne(baseUrl);
        expect(req.request.method).toBe('GET');
        req.flush(mockMovies);
    });

    it('should return empty array when no movies exist', () => {
        service.getMovies().subscribe((movies) => {
            expect(movies).toBeDefined();
            expect(movies.length).toBe(0);
            expect(movies).toEqual([]);
        });
        const req = httpMock.expectOne(baseUrl);
        expect(req.request.method).toBe('GET');
        req.flush([]);
    });

    it('should fetch movie by id successfully', () => {
        const testId = '1';
        service.getMovieById(testId).subscribe((movie) => {
            expect(movie).toBeDefined();
            expect(movie.id).toBe(testId);
            expect(movie).toEqual(mockMovie);
        });
        const req = httpMock.expectOne(`${baseUrl}/${testId}`);
        expect(req.request.method).toBe('GET');
        req.flush(mockMovie);
    });
});
