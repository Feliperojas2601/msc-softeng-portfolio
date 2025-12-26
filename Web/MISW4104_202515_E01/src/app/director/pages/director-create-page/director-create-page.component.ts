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
import { DirectorService } from '../../services/director.service';
import { InputFieldComponent } from '../../../shared/components/input-field/input-field.component';
import { CommonModule } from '@angular/common';
import { ToastrService } from 'ngx-toastr';

@Component({
    selector: 'app-director-create-page',
    imports: [CommonModule, ReactiveFormsModule, InputFieldComponent],
    templateUrl: './director-create-page.component.html',
    styleUrl: './director-create-page.component.css',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DirectorCreatePage {
    private readonly fb = inject(FormBuilder);
    private readonly directorService = inject(DirectorService);
    private readonly router = inject(Router);
    private readonly toastr = inject(ToastrService);

    public readonly isSubmitting = signal<boolean>(false);

    directorForm: FormGroup = this.fb.group({
        name: ['', [Validators.required]],
        birthDate: ['', [Validators.required]],
        nationality: ['', [Validators.required]],
        photo: ['', [Validators.required]],
        biography: ['', [Validators.required]],
    });

    getError(fieldName: string): string | null {
        const field = this.directorForm.get(fieldName);
        if (field?.invalid && (field?.dirty || field?.touched)) {
            if (field?.errors?.['required']) {
                return 'Este campo es requerido';
            }
        }
        return null;
    }

    onCancel(): void {
        this.directorForm.reset();
    }

    onSubmit(): void {
        if (this.directorForm.invalid) {
            Object.keys(this.directorForm.controls).forEach((key) => {
                this.directorForm.get(key)?.markAsTouched();
            });
            return;
        }
        this.isSubmitting.set(true);
        const formValue = this.directorForm.value;
        const directorData = {
            ...formValue,
            birthDate: new Date(formValue.birthDate).toISOString(),
        };
        this.directorService.createDirector(directorData).subscribe({
            next: (director) => {
                console.log('Director creado:', director);
                this.toastr.success(
                    `El director ${director.name} ha sido creado exitosamente`,
                    'Director creado',
                    { closeButton: true },
                );
                this.isSubmitting.set(false);
                this.directorForm.reset();
                this.router.navigate(['/director']);
            },
            error: (error) => {
                console.error('Error creando director:', error);
                this.isSubmitting.set(false);
            },
        });
    }
}
