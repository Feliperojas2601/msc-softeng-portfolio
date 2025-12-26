import { TestBed } from '@angular/core/testing';
import { ActorService } from './actor.service';
import { provideHttpClient } from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';
import { environment } from '../../../environments/environment.development';
import { faker } from '@faker-js/faker';
import { Actor } from '../interfaces/actor.interface';

describe('ActorService', () => {
    let service: ActorService;
    let httpMock: HttpTestingController;
    const baseUrl = environment.apiUrl + '/actors';
    const mockActors: Actor[] = Array.from({ length: 3 }, () => ({
        id: faker.string.uuid(),
        name: faker.person.fullName(),
        photo: faker.image.avatar(),
        nationality: faker.location.country(),
        birthDate: faker.date.past().toISOString(),
        biography: faker.lorem.paragraph(),
        movies: [],
    }));
    const mockActor: Actor = {
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
        service = TestBed.inject(ActorService);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should fetch actors successfully', () => {
        service.getActors().subscribe((actors) => {
            expect(actors).toBeDefined();
            expect(actors.length).toBe(3);
            expect(actors).toEqual(mockActors);
        });
        const req = httpMock.expectOne(baseUrl);
        expect(req.request.method).toBe('GET');
        req.flush(mockActors);
    });

    it('should return empty array when no actors exist', () => {
        service.getActors().subscribe((actors) => {
            expect(actors).toBeDefined();
            expect(actors.length).toBe(0);
            expect(actors).toEqual([]);
        });
        const req = httpMock.expectOne(baseUrl);
        expect(req.request.method).toBe('GET');
        req.flush([]);
    });

    it('should fetch actor by id successfully', () => {
        const testId = '1';
        service.getActorById(testId).subscribe((actor) => {
            expect(actor).toBeDefined();
            expect(actor.id).toBe(testId);
            expect(actor).toEqual(mockActor);
        });
        const req = httpMock.expectOne(`${baseUrl}/${testId}`);
        expect(req.request.method).toBe('GET');
        req.flush(mockActor);
    });
});
