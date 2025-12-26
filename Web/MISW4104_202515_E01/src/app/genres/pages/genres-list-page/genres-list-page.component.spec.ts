import { TestBed, ComponentFixture } from '@angular/core/testing';
import { GenresListPageComponent } from './genres-list-page.component';
import { provideHttpClient } from '@angular/common/http';
import { GenresService } from '../../services/genres.service';
import { of } from 'rxjs';
import { faker } from '@faker-js/faker';
import { Genre } from '../../interfaces/genre.interface';

describe('GenresListPageComponent', () => {
    let fixture: ComponentFixture<GenresListPageComponent>;
    let component: GenresListPageComponent;
    let compiled: HTMLElement;
    let genresService: GenresService;
    const mockGenres: Genre[] = Array.from({ length: 3 }, () => ({
        id: faker.string.uuid(),
        type: faker.music.genre(),
        movies: [
            {
                id: faker.string.uuid(),
                title: faker.lorem.words(3),
                poster: faker.image.url(),
                duration: faker.number.int({ min: 80, max: 180 }),
                country: faker.location.country(),
                releaseDate: faker.date.past().toISOString(),
                popularity: faker.number.float({ min: 0, max: 5 }),
            },
        ],
    }));

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [GenresListPageComponent],
            providers: [provideHttpClient()],
        });
        fixture = TestBed.createComponent(GenresListPageComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        genresService = TestBed.inject(GenresService);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
    it('should load genres on init', () => {
        spyOn(genresService, 'getGenres').and.returnValue(of(mockGenres));
        component.ngOnInit();
        expect(genresService.getGenres).toHaveBeenCalled();
        expect(component.genres().length).toBe(3);
        expect(component.isLoading()).toBe(false);
    });
    it('should toggle genre expansion', () => {
        const genreId = 'test-genre-id';
        expect(component.isGenreExpanded(genreId)).toBe(false);
        component.toggleGenre(genreId);
        expect(component.isGenreExpanded(genreId)).toBe(true);
        component.toggleGenre(genreId);
        expect(component.isGenreExpanded(genreId)).toBe(false);
    });
});
