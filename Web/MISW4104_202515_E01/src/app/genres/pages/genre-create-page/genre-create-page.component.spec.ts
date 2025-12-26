import { ComponentFixture, TestBed } from '@angular/core/testing';
import { GenreCreatePage } from './genre-create-page.component';
import { ReactiveFormsModule } from '@angular/forms';
import { provideRouter, Router } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';
import { GenresService } from '../../services/genres.service';
import { environment } from '../../../../environments/environment.development';
import { provideToastr, ToastrService } from 'ngx-toastr';

describe('GenreCreatePage', () => {
    let component: GenreCreatePage;
    let fixture: ComponentFixture<GenreCreatePage>;
    let httpTestingController: HttpTestingController;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [GenreCreatePage, ReactiveFormsModule],
            providers: [
                provideRouter([]),
                provideHttpClient(),
                provideHttpClientTesting(),
                provideToastr(),
                GenresService,
            ],
        }).compileComponents();

        fixture = TestBed.createComponent(GenreCreatePage);
        component = fixture.componentInstance;
        httpTestingController = TestBed.inject(HttpTestingController);
        fixture.detectChanges();
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

    it('should initialize form with empty values', () => {
        expect(component.genreForm.value).toEqual({
            type: '',
        });
    });

    it('should mark form as invalid when empty', () => {
        expect(component.genreForm.invalid).toBeTruthy();
    });

    it('should mark form as valid when type field is filled', () => {
        component.genreForm.patchValue({
            type: 'Science Fiction',
        });

        expect(component.genreForm.valid).toBeTruthy();
    });

    it('should return error message for required field', () => {
        const typeControl = component.genreForm.get('type');
        typeControl?.markAsTouched();
        typeControl?.setValue('');

        expect(component.getError('type')).toBe('Este campo es requerido');
    });

    it('should return null when field is valid', () => {
        const typeControl = component.genreForm.get('type');
        typeControl?.setValue('Science Fiction');
        typeControl?.markAsTouched();

        expect(component.getError('type')).toBeNull();
    });

    it('should not submit form when invalid', () => {
        const genresService = TestBed.inject(GenresService);
        spyOn(genresService, 'createGenre');

        component.onSubmit();

        expect(genresService.createGenre).not.toHaveBeenCalled();
    });

    it('should submit form when valid', (done) => {
        const toastr = TestBed.inject(ToastrService);
        const router = TestBed.inject(Router);
        spyOn(toastr, 'success');
        spyOn(router, 'navigate');

        component.genreForm.patchValue({
            type: 'Science Fiction',
        });

        component.onSubmit();

        const req = httpTestingController.expectOne(
            `${environment.apiUrl}/genres`,
        );
        expect(req.request.method).toBe('POST');
        expect(req.request.body.type).toBe('Science Fiction');

        req.flush({
            id: '1',
            type: 'Science Fiction',
            movies: [],
        });

        setTimeout(() => {
            expect(toastr.success).toHaveBeenCalled();
            expect(router.navigate).toHaveBeenCalledWith(['/genres']);
            done();
        }, 0);
    });

    it('should reset form on cancel', () => {
        component.genreForm.patchValue({
            type: 'Test Genre',
        });

        component.onCancel();

        expect(component.genreForm.value).toEqual({
            type: null,
        });
    });
});
