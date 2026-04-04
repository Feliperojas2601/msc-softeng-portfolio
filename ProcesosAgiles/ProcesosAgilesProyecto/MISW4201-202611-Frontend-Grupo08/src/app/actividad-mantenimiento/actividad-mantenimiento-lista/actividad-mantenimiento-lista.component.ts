import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ActividadMantenimiento } from '../actividad-mantenimiento';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ActividadMantenimientoService } from '../actividad-mantenimiento.service';
import { Component, OnInit, Input, ViewChild, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { EncabezadoComponent } from 'src/app/encabezado-app/encabezado/encabezado.component';
import { ActividadMantenimientoCrearComponent } from './actividad-mantenimiento-crear/actividad-mantenimiento-crear.component';
import { ActividadMantenimientoEditarComponent } from './actividad-mantenimiento-editar/actividad-mantenimiento-editar.component';


@Component({
    standalone: true,
    selector: 'app-actividad-mantenimiento-lista',
    templateUrl: './actividad-mantenimiento-lista.component.html',
    styleUrls: ['./actividad-mantenimiento-lista.component.css'],
    imports: [CommonModule, ReactiveFormsModule, EncabezadoComponent, ActividadMantenimientoCrearComponent, ActividadMantenimientoEditarComponent],
})
export class ActividadMantenimientoListaComponent implements OnInit {
    idPropiedad!: number;
    nombreActividadReciente: string = '';
    actividades: Array<ActividadMantenimiento> = [];
    actividadSeleccionada: ActividadMantenimiento | null = null;

    @ViewChild('modalConfirmarEliminar') modalConfirmarEliminar!: TemplateRef<any>;
    @ViewChild('modalEliminarConfirmado') modalEliminarConfirmadoTemplate!: TemplateRef<any>;

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private toastr: ToastrService,
        private modalService: NgbModal,
        private actividadService: ActividadMantenimientoService,
    ) { }

    ngOnInit(): void {
        this.idPropiedad = Number(this.route.snapshot.paramMap.get('id'));
        this.cargarActividades();
    }

    cargarActividades(): void {
        this.actividadService.darActividadesMantenimiento(this.idPropiedad).subscribe({
            next: (res) => {
                this.actividades = res;
                if (this.actividadSeleccionada) {
                    this.actividadSeleccionada = this.actividades.find(a => a.id === this.actividadSeleccionada!.id) ?? null;
                }
            },
            error: () => this.toastr.error("Error al cargar actividades")
        });
    }

    seleccionarActividad(actividad: ActividadMantenimiento): void {
        this.actividadSeleccionada = actividad;
    }

    abrirModalCrear(): void {
        const modalRef = this.modalService.open(ActividadMantenimientoCrearComponent, { size: 'lg', centered: true });
        modalRef.componentInstance.idPropiedad = this.idPropiedad;
        modalRef.result.then((result) => {
            if (result) {
                this.cargarActividades();
            }
        }).catch(() => {});
    }

    abrirModalEditar(actividad: ActividadMantenimiento): void {
        const modalRef = this.modalService.open(ActividadMantenimientoEditarComponent, { size: 'lg', centered: true });
        modalRef.componentInstance.idPropiedad = this.idPropiedad;
        modalRef.componentInstance.actividad = actividad;
        modalRef.result.then((result) => {
            if (result) {
                this.cargarActividades();
            }
        }).catch(() => {});
    }

    eliminarActividad(actividad: ActividadMantenimiento): void {
        this.nombreActividadReciente = actividad.concepto;
        const modalRef = this.modalService.open(this.modalConfirmarEliminar, { centered: true, size: 'sm' });
        modalRef.result.then((result) => {
            if (result === 'confirmar') {
                this.actividadService.eliminarActividadMantenimiento(this.idPropiedad, actividad.id).subscribe({
                    next: () => {
                        this.toastr.success("Actividad eliminada correctamente");
                        this.actividadSeleccionada = null;
                        this.cargarActividades();
                    },
                    error: (err) => {
                        const msg = err.error?.mensaje || "Error al eliminar la actividad";
                        this.toastr.error(msg);
                    }
                });
            }
        }).catch(() => {});
    }
}
