import { TestBed, ComponentFixture } from '@angular/core/testing';
import { MovieCardComponent } from './movie-card.component';
import { MovieCard } from '../../interfaces/movie.interface';
describe('MovieCardComponent', () => {
    let fixture: ComponentFixture<MovieCardComponent>;
    let component: MovieCardComponent;
    let compiled: HTMLElement;
    const mockMovie: MovieCard = {
        id: '1',
        title: 'Test Movie',
        poster: 'test-poster.jpg',
        popularity: 3.5,
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [MovieCardComponent],
        });
        fixture = TestBed.createComponent(MovieCardComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        fixture.componentRef.setInput('movie', mockMovie);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should display movie title and poster', () => {
        const title = compiled.querySelector('.card-title');
        const poster = compiled.querySelector('img') as HTMLImageElement;
        expect(title?.textContent).toContain('Test Movie');
        expect(poster?.src).toContain('test-poster.jpg');
        expect(poster?.alt).toBe('Test Movie');
    });

    it('should render 5 stars based on popularity', () => {
        const stars = compiled.querySelectorAll('.star');
        expect(stars.length).toBe(5);
        expect(component.isStarFilled(0)).toBe(true);
        expect(component.isStarFilled(1)).toBe(true);
        expect(component.isStarFilled(2)).toBe(true);
        expect(component.isStarHalf(3)).toBe(true);
        expect(component.isStarFilled(4)).toBe(false);
    });
});
