import { Propiedad } from '../propiedad';
import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { ErrorService } from 'src/app/error.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { PropiedadService } from '../propiedad.service';
import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';
import { ActivatedRoute, Router, RouterModule, RouterLink } from '@angular/router';
import { PropiedadCrearComponent } from '../propiedad-crear/propiedad-crear.component';
import { PropiedadEditarComponent } from '../propiedad-editar/propiedad-editar.component';
import { EncabezadoComponent } from '../../encabezado-app/encabezado/encabezado.component';

@Component({
    selector: 'app-propiedad-lista',
    standalone: true,
    imports: [CommonModule, EncabezadoComponent, RouterModule, RouterLink, ReactiveFormsModule, PropiedadCrearComponent, PropiedadEditarComponent],
    templateUrl: './propiedad-lista.component.html',
    styleUrls: ['./propiedad-lista.component.css']
})
export class PropiedadListaComponent implements OnInit {
    propiedades: Array<Propiedad> = []
    @ViewChild('modalConfirmarEliminar') modalConfirmarEliminar!: TemplateRef<any>;

    constructor(
        private readonly routerPath: Router,
        private readonly toastr: ToastrService,
        private readonly modalService: NgbModal,
        private readonly propiedadService: PropiedadService,
        private readonly errorService: ErrorService
    ) { }

    ngOnInit() {
        this.cargarPropiedades();
    }

    cargarPropiedades(): void {
        this.propiedadService.darPropiedades().subscribe({
            next: (propiedades) => {
                this.propiedades = propiedades;
            },
            error: (error) => this.errorService.manejarError(error)
        });
    }

    abrirModalCrear(): void {
        const modalRef = this.modalService.open(PropiedadCrearComponent, {
            size: 'lg',
            centered: true
        });

        // Escuchamos el resultado del modal
        modalRef.result.then((result) => {
            if (result) {
                // Si el modal cerró con éxito, recargamos la lista
                this.cargarPropiedades();
            }
        }).catch(() => {
            // El usuario canceló o cerró el modal, no hacemos nada
        });
    }

    reservas(idPropiedad: number): void {
        this.routerPath.navigate(['/propiedades/' + idPropiedad + '/reservas']);
    }

    movimientos(idPropiedad: number): void {
        this.routerPath.navigate(['/propiedades/'+ idPropiedad + '/movimientos']);
    }

    elementospropiedad(idPropiedad: number): void {
        this.routerPath.navigate(['/propiedades/' + idPropiedad + '/elementos_propiedad']);
    }

    actividadesmantenimiento(idPropiedad: number): void {
        this.routerPath.navigate(['/propiedades/' + idPropiedad + '/actividades']);
    }

    editarPropiedad(idPropiedad: number): void {
        const modalRef = this.modalService.open(PropiedadEditarComponent, {
            size: 'lg',
            centered: true
        });
        
        modalRef.componentInstance.idPropiedad = idPropiedad;
        
        // Escuchamos el resultado del modal
        modalRef.result.then((result) => {
            if (result) {
                // Si el modal cerró con éxito, recargamos la lista
                this.cargarPropiedades();
            }
        }).catch(() => {
            // El usuario canceló o cerró el modal, no hacemos nada
        });
    }

    eliminarPropiedad(propiedad: Propiedad): void {
        
        // 2. ABRIMOS el modal de confirmación que creaste en el HTML
        const modalRef = this.modalService.open(this.modalConfirmarEliminar, { centered: true, size: 'sm' });
    
        // 3. Escuchamos la respuesta del modal
        modalRef.result.then((result) => {
          if (result === 'confirmar') {
            // Si el usuario confirmó, llamamos al servicio
           this.propiedadService.borrarPropiedad(propiedad.id).subscribe({
              next: () => {
                this.toastr.success("Propiedad eliminado correctamente");
                this.ngOnInit();
              },
              error: () => this.toastr.error("Error al eliminar el elemento")
            });
          }
        }).catch(() => {
          // En caso de cancelar, no se aplicaran cambios
        });
    }

}
