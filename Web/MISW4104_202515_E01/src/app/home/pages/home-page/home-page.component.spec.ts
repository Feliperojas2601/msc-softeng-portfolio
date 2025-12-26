import { TestBed, ComponentFixture } from '@angular/core/testing';
import { HomePageComponent } from './home-page.component';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { MovieService } from '../../../movie/services/movie.service';
import { of, throwError } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Movie } from '../../../movie/interfaces/movie.interface';

describe('HomePageComponent', () => {
    let fixture: ComponentFixture<HomePageComponent>;
    let component: HomePageComponent;
    let compiled: HTMLElement;
    let movieService: MovieService;

    const mockMovies: Movie[] = Array.from({ length: 12 }, (_, index) => ({
        id: faker.string.uuid(),
        title: faker.lorem.words(3),
        poster: faker.image.url(),
        duration: faker.number.int({ min: 80, max: 180 }),
        country: faker.location.country(),
        releaseDate: faker.date.past().toISOString(),
        popularity: 5 - index * 0.3, // Popularidad decreciente
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
            imports: [HomePageComponent],
            providers: [provideHttpClient(), provideRouter([])],
        });
        fixture = TestBed.createComponent(HomePageComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        movieService = TestBed.inject(MovieService);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should load and display popular movies sorted by popularity', () => {
        const unsortedMovies = [
            { ...mockMovies[0], popularity: 2.5 },
            { ...mockMovies[1], popularity: 4.8 },
            { ...mockMovies[2], popularity: 3.2 },
        ];
        spyOn(movieService, 'getMovies').and.returnValue(of(unsortedMovies));

        component.ngOnInit();
        fixture.detectChanges();

        expect(movieService.getMovies).toHaveBeenCalled();
        expect(component.popularMovies().length).toBe(3);
        expect(component.isLoading()).toBe(false);
        expect(component.popularMovies()[0].popularity).toBe(4.8);
        expect(component.popularMovies()[1].popularity).toBe(3.2);
        expect(component.popularMovies()[2].popularity).toBe(2.5);

        const title = compiled.querySelector('.page-title');
        expect(title?.textContent).toContain(
            'Explora las películas más populares',
        );
    });

    it('should navigate carousel slides correctly', () => {
        component.popularMovies.set(mockMovies);
        component.currentIndex.set(0);

        component.nextSlide();
        expect(component.currentIndex()).toBe(1);

        component.previousSlide();
        expect(component.currentIndex()).toBe(0);

        component.previousSlide();
        expect(component.currentIndex()).toBe(0);

        const maxIndex = component.maxIndex();
        component.currentIndex.set(maxIndex);
        component.nextSlide();
        expect(component.currentIndex()).toBe(maxIndex);
    });
});
