import { TestBed, ComponentFixture } from '@angular/core/testing';
import { DirectorListPageComponent } from './director-list-page.component';
import { provideHttpClient } from '@angular/common/http';
import { DirectorService } from '../../services/director.service';
import { of } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Director } from '../../interfaces/director.interface';

describe('ActorListPageComponent', () => {
    let fixture: ComponentFixture<DirectorListPageComponent>;
    let component: DirectorListPageComponent;
    let compiled: HTMLElement;
    let directorService: DirectorService;
    const mockActors: Director[] = Array.from({ length: 3 }, () => ({
        id: faker.string.uuid(),
        name: faker.person.fullName(),
        photo: faker.image.avatar(),
        nationality: faker.location.country(),
        birthDate: faker.date.past().toISOString(),
        biography: faker.lorem.paragraph(),
        movies: [],
    }));

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [DirectorListPageComponent],
            providers: [provideHttpClient()],
        });
        fixture = TestBed.createComponent(DirectorListPageComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        directorService = TestBed.inject(DirectorService);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should display title and search input', () => {
        fixture.detectChanges();
        const title = compiled.querySelector('h2');
        const searchInput = compiled.querySelector(
            'input[type="text"]',
        ) as HTMLInputElement;
        expect(title?.textContent).toContain('Directores destacados');
        expect(searchInput).toBeTruthy();
        expect(searchInput?.placeholder).toBe('Búsqueda');
    });

    it('should load directors on init', () => {
        spyOn(directorService, 'getDirectors').and.returnValue(of(mockActors));
        component.ngOnInit();
        expect(directorService.getDirectors).toHaveBeenCalled();
        expect(component.directors().length).toBe(3);
        expect(component.isLoading()).toBe(false);
    });
});
