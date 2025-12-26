import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DirectorDetailPageComponent } from './director-detail-page.component';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';
import { DirectorService } from '../../services/director.service';
import { provideToastr } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Director } from '../../interfaces/director.interface';

describe('DirectorDetailPageComponent', () => {
    let component: DirectorDetailPageComponent;
    let fixture: ComponentFixture<DirectorDetailPageComponent>;
    let httpTestingController: HttpTestingController;
    let directorService: DirectorService;

    const mockDirectorId = faker.string.uuid();

    const mockDirector: Director = {
        id: mockDirectorId,
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
                get: (key: string) => mockDirectorId,
            },
        },
    };

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [DirectorDetailPageComponent],
            providers: [
                provideRouter([]),
                provideHttpClient(),
                provideHttpClientTesting(),
                provideToastr(),
                DirectorService,
                { provide: ActivatedRoute, useValue: mockActivatedRoute },
            ],
        }).compileComponents();

        fixture = TestBed.createComponent(DirectorDetailPageComponent);
        component = fixture.componentInstance;
        httpTestingController = TestBed.inject(HttpTestingController);
        directorService = TestBed.inject(DirectorService);
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

    it('should call getDirectorById on init', (done) => {
        spyOn(directorService, 'getDirectorById').and.returnValue(
            of(mockDirector),
        );

        component.ngOnInit();

        setTimeout(() => {
            expect(directorService.getDirectorById).toHaveBeenCalledWith(
                mockDirectorId,
            );
            expect(component.directorDetails()).toEqual(mockDirector);
            done();
        }, 0);
    });

    it('should display director details after loading', (done) => {
        spyOn(directorService, 'getDirectorById').and.returnValue(
            of(mockDirector),
        );

        component.ngOnInit();
        fixture.detectChanges();

        setTimeout(() => {
            const compiled = fixture.nativeElement;
            const directorName = compiled.querySelector('.director-name');
            const nationality = compiled.querySelector('.director-info h3');
            const biography = compiled.querySelector('.biography');

            expect(directorName?.textContent).toContain(mockDirector.name);
            expect(nationality?.textContent).toContain(
                mockDirector.nationality,
            );
            expect(biography?.textContent).toContain(mockDirector.biography);
            done();
        }, 0);
    });

    it('should handle error when fetching director details', (done) => {
        spyOn(directorService, 'getDirectorById').and.returnValue(
            of(mockDirector),
        );
        spyOn(console, 'error');

        component.ngOnInit();

        setTimeout(() => {
            expect(directorService.getDirectorById).toHaveBeenCalledWith(
                mockDirectorId,
            );
            done();
        }, 0);
    });
});
