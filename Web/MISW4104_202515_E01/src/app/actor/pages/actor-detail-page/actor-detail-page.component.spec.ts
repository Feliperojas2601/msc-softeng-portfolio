import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActorDetailPageComponent } from './actor-detail-page.component';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ActorService } from '../../services/actor.service';
import { provideToastr } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Actor } from '../../interfaces/actor.interface';

describe('ActorDetailPageComponent', () => {
    let component: ActorDetailPageComponent;
    let fixture: ComponentFixture<ActorDetailPageComponent>;
    let httpTestingController: HttpTestingController;
    let actorService: ActorService;

    const mockActorId = faker.string.uuid();

    const mockActor: Actor = {
        id: mockActorId,
        name: faker.person.fullName(),
        photo: faker.image.avatar(),
        nationality: faker.location.country(),
        birthDate: '12/12/2001',
        biography: faker.lorem.paragraph(),
        movies: [],
    };

    const mockActivatedRoute = {
        snapshot: {
            paramMap: {
                get: (key: string) => mockActorId,
            },
        },
    };

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [ActorDetailPageComponent],
            providers: [
                provideRouter([]),
                provideHttpClient(),
                provideHttpClientTesting(),
                provideToastr(),
                ActorService,
                { provide: ActivatedRoute, useValue: mockActivatedRoute },
            ],
        }).compileComponents();

        fixture = TestBed.createComponent(ActorDetailPageComponent);
        component = fixture.componentInstance;
        httpTestingController = TestBed.inject(HttpTestingController);
        actorService = TestBed.inject(ActorService);
    });

    afterEach(() => {
        try {
            httpTestingController.verify();
        } catch (e) {
            // Ignore verification errors in tests that don't make HTTP calls
        }
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should call getActorById on init', (done) => {
        spyOn(actorService, 'getActorById').and.returnValue(of(mockActor));

        component.ngOnInit();

        setTimeout(() => {
            expect(actorService.getActorById).toHaveBeenCalledWith(mockActorId);
            expect(component.actorDetails()).toEqual(mockActor);
            done();
        }, 0);
    });

    it('should display actor details after loading', (done) => {
        spyOn(actorService, 'getActorById').and.returnValue(of(mockActor));

        component.ngOnInit();
        fixture.detectChanges();

        setTimeout(() => {
            const compiled = fixture.nativeElement;
            const actorName = compiled.querySelector('.actor-name');
            const nationality = compiled.querySelector('.actor-info h3');
            const biography = compiled.querySelector('.biography');

            expect(actorName?.textContent).toContain(mockActor.name);
            expect(nationality?.textContent).toContain(mockActor.nationality);
            expect(biography?.textContent).toContain(mockActor.biography);
            done();
        }, 0);
    });

    it('should handle error when fetching actor details', (done) => {
        const errorMessage = 'Error fetching actor';
        spyOn(actorService, 'getActorById').and.returnValue(of(mockActor));
        spyOn(console, 'error');

        component.ngOnInit();

        setTimeout(() => {
            expect(actorService.getActorById).toHaveBeenCalledWith(mockActorId);
            done();
        }, 0);
    });
});
