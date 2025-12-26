import { TestBed, ComponentFixture } from '@angular/core/testing';
import { MovieListPageComponent } from './movie-list-page.component';
import { provideHttpClient } from '@angular/common/http';
import { MovieService } from '../../services/movie.service';
import { of } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Movie } from '../../interfaces/movie.interface';

describe('MovieListPageComponent', () => {
    let fixture: ComponentFixture<MovieListPageComponent>;
    let component: MovieListPageComponent;
    let compiled: HTMLElement;
    let movieService: MovieService;
    const mockMovies: Movie[] = Array.from({ length: 3 }, () => ({
        id: faker.string.uuid(),
        title: faker.lorem.words(3),
        poster: faker.image.url(),
        duration: faker.number.int({ min: 80, max: 180 }),
        country: faker.location.country(),
        releaseDate: faker.date.past().toISOString(),
        popularity: faker.number.float({ min: 0, max: 5 }),
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
            type: 'Action',
        },
        platforms: [],
        reviews: [],
        youtubeTrailer: {
            id: faker.string.uuid(),
            name: faker.lorem.words(3),
            url: faker.internet.url(),
            duration: faker.number.int({ min: 60, max: 180 }),
            channel: faker.company.name(),
        },
    }));

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [MovieListPageComponent],
            providers: [provideHttpClient()],
        });
        fixture = TestBed.createComponent(MovieListPageComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        movieService = TestBed.inject(MovieService);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should display title, search input and genre dropdown', () => {
        fixture.detectChanges();
        const title = compiled.querySelector('h2');
        const searchInput = compiled.querySelector(
            'input[type="text"]',
        ) as HTMLInputElement;
        const dropdownButton = compiled.querySelector('.dropdown button');
        expect(title?.textContent).toContain('Películas increíbles');
        expect(searchInput).toBeTruthy();
        expect(searchInput?.placeholder).toBe('Búsqueda');
        expect(dropdownButton).toBeTruthy();
    });

    it('should load movies on init and toggle dropdown', () => {
        spyOn(movieService, 'getMovies').and.returnValue(of(mockMovies));
        component.ngOnInit();
        expect(movieService.getMovies).toHaveBeenCalled();
        expect(component.movies().length).toBe(3);
        expect(component.isLoading()).toBe(false);
        expect(component.showDropdown()).toBe(false);
        component.toggleDropdown();
        expect(component.showDropdown()).toBe(true);
    });

    it('should filter movies by genre', () => {
        const actionMovies: Movie[] = [
            {
                ...mockMovies[0],
                genre: { id: '1', type: 'Action' },
            },
            {
                ...mockMovies[1],
                genre: { id: '2', type: 'Action' },
            },
        ];
        const dramaMovies: Movie[] = [
            {
                ...mockMovies[2],
                genre: { id: '3', type: 'Drama' },
            },
        ];
        const allMovies = [...actionMovies, ...dramaMovies];
        component.cachedMovies.set(allMovies);
        component.movies.set(allMovies);
        component.onFilterByGenre('Action');
        expect(component.movies().length).toBe(2);
        expect(component.movies().every((m) => m.genre.type === 'Action')).toBe(
            true,
        );
        expect(component.selectedGenre()).toBe('Action');
        expect(component.showDropdown()).toBe(false);
        component.onFilterByGenre('Todos');
        expect(component.movies().length).toBe(3);
    });
});
