import { TestBed } from '@angular/core/testing';
import { DirectorService } from './director.service';
import { provideHttpClient } from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';
import { environment } from '../../../environments/environment.development';
import { faker } from '@faker-js/faker';
import { Director } from '../interfaces/director.interface';

describe('DirectorService', () => {
    let service: DirectorService;
    let httpMock: HttpTestingController;
    const baseUrl = environment.apiUrl + '/directors';
    const mockDirectors: Director[] = Array.from({ length: 3 }, () => ({
        id: faker.string.uuid(),
        name: faker.person.fullName(),
        photo: faker.image.avatar(),
        nationality: faker.location.country(),
        birthDate: faker.date.past().toISOString(),
        biography: faker.lorem.paragraph(),
        movies: [],
    }));
    const mockDirector: Director = {
        id: '1',
        name: faker.person.fullName(),
        photo: faker.image.avatar(),
        nationality: faker.location.country(),
        birthDate: faker.date.past().toISOString(),
        biography: faker.lorem.paragraph(),
        movies: [],
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [provideHttpClient(), provideHttpClientTesting()],
        });
        service = TestBed.inject(DirectorService);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should fetch directors successfully', () => {
        service.getDirectors().subscribe((directors) => {
            expect(directors).toBeDefined();
            expect(directors.length).toBe(3);
            expect(directors).toEqual(mockDirectors);
        });
        const req = httpMock.expectOne(baseUrl);
        expect(req.request.method).toBe('GET');
        req.flush(mockDirectors);
    });

    it('should return empty array when no directors exist', () => {
        service.getDirectors().subscribe((directors) => {
            expect(directors).toBeDefined();
            expect(directors.length).toBe(0);
            expect(directors).toEqual([]);
        });
        const req = httpMock.expectOne(baseUrl);
        expect(req.request.method).toBe('GET');
        req.flush([]);
    });

    it('should fetch director by id successfully', () => {
        const testId = '1';
        service.getDirectorById(testId).subscribe((director) => {
            expect(director).toBeDefined();
            expect(director.id).toBe(testId);
            expect(director).toEqual(mockDirector);
        });
        const req = httpMock.expectOne(`${baseUrl}/${testId}`);
        expect(req.request.method).toBe('GET');
        req.flush(mockDirector);
    });
});
