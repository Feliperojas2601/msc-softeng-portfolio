import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { TipoEstado } from 'src/app/enums';
import { CommonModule } from '@angular/common';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ElementoPropiedad } from '../../elemento-propiedad';
import { ElementoPropiedadService } from '../../elemento-propiedad.service';
import { Component, OnInit, Input, ViewChild, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
    standalone: true,
    selector: 'app-elemento-propiedad-editar',
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './elemento-propiedad-editar.component.html',
    styleUrl: './elemento-propiedad-editar.component.css'
})
export class ElementoPropiedadEditarComponent implements OnInit {
    elementoForm!: FormGroup;
    @Input() idPropiedad!: number;
    elementos: ElementoPropiedad[] = [];
    estados = Object.values(TipoEstado);
    nombreElementoReciente: string = '';
    @Input() elementoExistente?: ElementoPropiedad;
    @ViewChild('modalExito') modalExito!: TemplateRef<any>;

    constructor(
        private fb: FormBuilder,
        private router: Router,
        public modalService: NgbModal,
        private toastr: ToastrService,
        public activeModal: NgbActiveModal,
        private elementoService: ElementoPropiedadService,
    ) { }

    ngOnInit(): void {
        this.elementoForm = this.fb.group({
            nombre: ["", [Validators.required, Validators.maxLength(40)]],
            tipo: ["", [Validators.required, Validators.maxLength(40)]],
            estado: [null, [Validators.required]],
            descripcion: ["", [Validators.required, Validators.maxLength(125)]],
            zona: ["", [Validators.required, Validators.maxLength(80)]],
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
            this.router.navigate(['/propiedades', this.idPropiedad, 'elementos_propiedad']);

            // Refrescar la vista o limpiar estados:
            this.obtenerElementos();

        }).catch(() => {

            // Por si cierran con la X o ESC
            this.obtenerElementos();
        });
    }

    editar(): void {
        console.log("Datos enviados a Flask:", this.elementoForm.value);
        if (this.elementoForm.invalid || !this.elementoExistente) {
            this.toastr.warning("Formulario incompleto o sin referencia de elemento");
            return;
        }

        this.elementoService.editarElementoPropiedad(this.idPropiedad, this.elementoForm.value, this.elementoExistente.id).subscribe({
            next: (res) => {
                this.toastr.success("Elemento actualizado");
                this.activeModal.close(res);
                this.mostrarAvisoExito(res.nombre);
            },
            error: (err) => {
                this.toastr.error("Error al actualizar")
                console.error("Error en Flask:", err);
            }
        });
    }
}