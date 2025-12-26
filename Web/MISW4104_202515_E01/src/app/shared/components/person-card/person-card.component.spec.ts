import { TestBed, ComponentFixture } from '@angular/core/testing';
import { PersonCardComponent } from './person-card.component';
import { Actor } from '../../../actor/interfaces/actor.interface';

describe('PersonCardComponent', () => {
    let fixture: ComponentFixture<PersonCardComponent>;
    let component: PersonCardComponent;
    let compiled: HTMLElement;
    const mockActor: Actor = {
        id: '1',
        name: 'Test Actor',
        photo: 'test-photo.jpg',
        nationality: 'American',
        birthDate: '1990-01-01',
        biography: 'Test biography',
        movies: [
            {
                id: '1',
                title: 'Test Movie',
                poster: 'test-poster.jpg',
                duration: 120,
                country: 'USA',
                releaseDate: '2020-01-01',
                popularity: 4.5,
            },
        ],
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [PersonCardComponent],
        });
        fixture = TestBed.createComponent(PersonCardComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        fixture.componentRef.setInput('person', mockActor);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should display actor name, photo and nationality', () => {
        const name = compiled.querySelector('.card-title');
        const nationality = compiled.querySelector('.card-text');
        const photo = compiled.querySelector('img') as HTMLImageElement;
        expect(name?.textContent).toContain('Test Actor');
        expect(nationality?.textContent).toContain('American');
        expect(photo?.src).toContain('test-photo.jpg');
        expect(photo?.alt).toBe('Test Actor');
    });

    it('should toggle movies visibility when button is clicked', () => {
        expect(component.showMovies()).toBe(false);
        const button = compiled.querySelector('button');
        button?.click();
        expect(component.showMovies()).toBe(true);
        button?.click();
        expect(component.showMovies()).toBe(false);
    });
});
