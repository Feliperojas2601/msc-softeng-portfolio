import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { TipoEstado } from 'src/app/enums';
import { CommonModule } from '@angular/common';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ElementoPropiedad } from '../../elemento-propiedad';
import { Component, OnInit, Input, ViewChild, TemplateRef } from '@angular/core';
import { ElementoPropiedadService } from '../../elemento-propiedad.service';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, Validators, ReactiveFormsModule } from '@angular/forms';

function noSoloEspacios(control: AbstractControl): ValidationErrors | null {
    const val = control.value;
    if (val && typeof val === 'string' && val.trim().length === 0) {
        return { soloEspacios: true };
    }
    return null;
}

@Component({
    selector: 'app-elemento-propiedad-crear',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './elemento-propiedad-crear.component.html',
    styleUrl: './elemento-propiedad-crear.component.css'
})
export class ElementoPropiedadCrearComponent implements OnInit {
    elementoForm!: FormGroup;
    @Input() idPropiedad!: number;
    elementos: ElementoPropiedad[] = [];
    estados = Object.values(TipoEstado);
    nombreElementoReciente: string = '';
    @Input() elementoExistente?: ElementoPropiedad;
    @ViewChild('modalExito') modalExito!: TemplateRef<any>;

    constructor(
        private router: Router,
        private fb: FormBuilder,
        public modalService: NgbModal,
        private toastr: ToastrService,
        public activeModal: NgbActiveModal,
        private elementoService: ElementoPropiedadService,
    ) { }

    ngOnInit(): void {
        this.elementoForm = this.fb.group({
            nombre: ["", [Validators.required, noSoloEspacios, Validators.maxLength(40)]],
            tipo: ["", [Validators.required, noSoloEspacios, Validators.maxLength(40)]],
            estado: [null, [Validators.required]],
            descripcion: ["", [Validators.required, noSoloEspacios, Validators.maxLength(125)]],
            zona: ["", [Validators.required, noSoloEspacios, Validators.maxLength(80)]],
            fecha_registro: [new Date().toISOString().split('T')[0], [Validators.required]]
        });

        if (this.elementoExistente) {
            this.elementoForm.patchValue(this.elementoExistente);
        }
    }

    obtenerElementos() {
        this.elementoService.darElementosPropiedad(this.idPropiedad).subscribe({
            next: (res) => this.elementos = res,
            error: (err) => this.toastr.error(`Error {${err.statusText}} al cargar la lista`)
        });
    }

    mostrarAvisoExito(nombre: string) {

        // Guardamos el nombre del elemento recién creado
        this.nombreElementoReciente = nombre;

        // Presentación del modal
        const modalRef = this.modalService.open(this.modalExito, { centered: true, size: 'sm' });

        // Redirigir al menú de elementos de la propiedad
        modalRef.result.then(() => {

            // Navegación a la propiedad
            this.router.navigate(['/propiedades', this.idPropiedad, '/elementos_propiedad']);

            // Refrescar la vista o limpiar estados:
            this.obtenerElementos();

        }).catch(() => {

            // Por si cierran con la X o ESC
            this.obtenerElementos();
        });
    }

    guardar(): void {
        if (this.elementoForm.invalid) {
            this.elementoForm.markAllAsTouched();
            this.toastr.error("Por favor completa todos los campos requeridos.", "Formulario incompleto");
            return;
        }

        this.elementoService.crearElementoPropiedad(this.idPropiedad, this.elementoForm.value).subscribe({
            next: (res) => {
                this.toastr.success("Elemento registrado");
                this.activeModal.close(res);
                this.mostrarAvisoExito(res.nombre);
            },
            error: (err) => {
                console.error("Error en Flask:", err);
                this.toastr.error("Error al registrar el elemento");
            }
        });
    }
}