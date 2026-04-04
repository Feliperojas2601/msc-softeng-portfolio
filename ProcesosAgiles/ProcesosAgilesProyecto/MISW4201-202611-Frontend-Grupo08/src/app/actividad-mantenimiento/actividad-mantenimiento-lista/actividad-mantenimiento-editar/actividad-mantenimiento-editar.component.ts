import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ActividadMantenimiento } from '../../actividad-mantenimiento';
import { Component, OnInit, Input } from '@angular/core';
import { ActividadMantenimientoService } from '../../actividad-mantenimiento.service';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { EnumsService } from 'src/app/enums.service';

@Component({
    standalone: true,
    selector: 'app-actividad-mantenimiento-editar',
    templateUrl: './actividad-mantenimiento-editar.component.html',
    styleUrls: ['./actividad-mantenimiento-editar.component.css'],
    imports: [CommonModule, ReactiveFormsModule]
})
export class ActividadMantenimientoEditarComponent implements OnInit {
    @Input() idPropiedad!: number;
    @Input() actividad!: ActividadMantenimiento;

    categorias: string[] = [];
    periodicidades: string[] = [];
    editarForm!: FormGroup;
    errorDuplicado: string = '';

    constructor(
        private fb: FormBuilder,
        public activeModal: NgbActiveModal,
        private toastr: ToastrService,
        private actividadService: ActividadMantenimientoService,
        private enumService: EnumsService
    ) {}

    ngOnInit(): void {
        this.editarForm = this.fb.group({
            concepto: [this.actividad.concepto, [Validators.required]],
            categoria: [this.actividad.categoria, []],
            periodicidad: [this.actividad.periodicidad, [Validators.required]],
            costo: [this.actividad.costo, [Validators.required, Validators.maxLength(80)]]
        });

        this.enumService.tipoCategoriaMantenimiento().subscribe((cats: any) => {
            this.categorias = cats;
            this.editarForm.patchValue({ categoria: this.actividad.categoria });
        });

        this.enumService.periodicidadMantenimiento().subscribe((pers: any) => {
            this.periodicidades = pers;
            this.editarForm.patchValue({ periodicidad: this.actividad.periodicidad });
        });
    }

    guardar(): void {
        if (this.editarForm.invalid) return;
        this.errorDuplicado = '';
        this.actividadService.editarActividadMantenimiento(this.idPropiedad, this.actividad.id, this.editarForm.value).subscribe({
            next: (res) => {
                this.toastr.success('Actividad actualizada correctamente');
                this.activeModal.close(res);
            },
            error: (err) => {
                if (err.status === 409) {
                    this.errorDuplicado = err.error?.mensaje || 'Ya existe una actividad con ese concepto en esta propiedad';
                } else {
                    this.toastr.error('Error al actualizar la actividad');
                }
            }
        });
    }
}
