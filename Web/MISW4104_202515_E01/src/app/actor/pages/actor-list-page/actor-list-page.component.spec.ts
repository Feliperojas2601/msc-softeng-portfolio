import { TestBed, ComponentFixture } from '@angular/core/testing';
import { ActorListPageComponent } from './actor-list-page.component';
import { provideHttpClient } from '@angular/common/http';
import { ActorService } from '../../services/actor.service';
import { of } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Actor } from '../../interfaces/actor.interface';
describe('ActorListPageComponent', () => {
    let fixture: ComponentFixture<ActorListPageComponent>;
    let component: ActorListPageComponent;
    let compiled: HTMLElement;
    let actorService: ActorService;
    const mockActors: Actor[] = Array.from({ length: 3 }, () => ({
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
            imports: [ActorListPageComponent],
            providers: [provideHttpClient()],
        });
        fixture = TestBed.createComponent(ActorListPageComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        actorService = TestBed.inject(ActorService);
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
        expect(title?.textContent).toContain('Actores destacados');
        expect(searchInput).toBeTruthy();
        expect(searchInput?.placeholder).toBe('Búsqueda');
    });

    it('should load actors on init', () => {
        spyOn(actorService, 'getActors').and.returnValue(of(mockActors));
        component.ngOnInit();
        expect(actorService.getActors).toHaveBeenCalled();
        expect(component.actors().length).toBe(3);
        expect(component.isLoading()).toBe(false);
    });
});
