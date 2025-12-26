import {
    ChangeDetectionStrategy,
    Component,
    inject,
    signal,
} from '@angular/core';
import {
    FormBuilder,
    FormGroup,
    Validators,
    ReactiveFormsModule,
} from '@angular/forms';
import { Router } from '@angular/router';
import { GenresService } from '../../services/genres.service';
import { InputFieldComponent } from '../../../shared/components/input-field/input-field.component';
import { CommonModule } from '@angular/common';
import { ToastrService } from 'ngx-toastr';

@Component({
    selector: 'app-genre-create-page',
    imports: [CommonModule, ReactiveFormsModule, InputFieldComponent],
    templateUrl: './genre-create-page.component.html',
    styleUrl: './genre-create-page.component.css',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GenreCreatePage {
    private readonly fb = inject(FormBuilder);
    private readonly genresService = inject(GenresService);
    private readonly router = inject(Router);
    private readonly toastr = inject(ToastrService);

    public readonly isSubmitting = signal<boolean>(false);

    genreForm: FormGroup = this.fb.group({
        type: ['', [Validators.required]],
    });

    getError(fieldName: string): string | null {
        const field = this.genreForm.get(fieldName);
        if (field?.invalid && (field?.dirty || field?.touched)) {
            if (field?.errors?.['required']) {
                return 'Este campo es requerido';
            }
        }
        return null;
    }

    onCancel(): void {
        this.genreForm.reset();
    }

    onSubmit(): void {
        if (this.genreForm.invalid) {
            Object.keys(this.genreForm.controls).forEach((key) => {
                this.genreForm.get(key)?.markAsTouched();
            });
            return;
        }
        this.isSubmitting.set(true);
        const genreData = {
            type: this.genreForm.value.type,
        };
        this.genresService.createGenre(genreData).subscribe({
            next: (genre) => {
                console.log('Género creado:', genre);
                this.toastr.success(
                    `El género ${genre.type} ha sido creado exitosamente`,
                    'Género creado',
                    { closeButton: true },
                );
                this.isSubmitting.set(false);
                this.genreForm.reset();
                this.router.navigate(['/genres']);
            },
            error: (error) => {
                console.error('Error creando género:', error);
                this.isSubmitting.set(false);
            },
        });
    }
}
