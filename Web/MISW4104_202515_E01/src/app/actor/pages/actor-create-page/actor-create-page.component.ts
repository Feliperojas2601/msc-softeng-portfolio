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
import { ActorService } from '../../services/actor.service';
import { InputFieldComponent } from '../../../shared/components/input-field/input-field.component';
import { CommonModule } from '@angular/common';
import { ToastrService } from 'ngx-toastr';

@Component({
    selector: 'app-actor-create-page',
    imports: [CommonModule, ReactiveFormsModule, InputFieldComponent],
    templateUrl: './actor-create-page.component.html',
    styleUrl: './actor-create-page.component.css',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ActorCreatePage {
    private readonly fb = inject(FormBuilder);
    private readonly actorService = inject(ActorService);
    private readonly router = inject(Router);
    private readonly toastr = inject(ToastrService);

    public readonly isSubmitting = signal<boolean>(false);

    actorForm: FormGroup = this.fb.group({
        name: ['', [Validators.required]],
        birthDate: ['', [Validators.required]],
        nationality: ['', [Validators.required]],
        photo: ['', [Validators.required]],
        biography: ['', [Validators.required]],
    });

    getError(fieldName: string): string | null {
        const field = this.actorForm.get(fieldName);
        if (field?.invalid && (field?.dirty || field?.touched)) {
            if (field?.errors?.['required']) {
                return 'Este campo es requerido';
            }
        }
        return null;
    }

    onCancel(): void {
        this.actorForm.reset();
    }

    onSubmit(): void {
        if (this.actorForm.invalid) {
            Object.keys(this.actorForm.controls).forEach((key) => {
                this.actorForm.get(key)?.markAsTouched();
            });
            return;
        }
        this.isSubmitting.set(true);
        const formValue = this.actorForm.value;
        const actorData = {
            ...formValue,
            birthDate: new Date(formValue.birthDate).toISOString(),
        };
        this.actorService.createActor(actorData).subscribe({
            next: (actor) => {
                console.log('Actor creado:', actor);
                this.toastr.success(
                    `El actor ${actor.name} ha sido creado exitosamente`,
                    'Actor creado',
                    { closeButton: true },
                );
                this.isSubmitting.set(false);
                this.actorForm.reset();
                this.router.navigate(['/actor']);
            },
            error: (error) => {
                console.error('Error creando actor:', error);
                this.isSubmitting.set(false);
            },
        });
    }
}
