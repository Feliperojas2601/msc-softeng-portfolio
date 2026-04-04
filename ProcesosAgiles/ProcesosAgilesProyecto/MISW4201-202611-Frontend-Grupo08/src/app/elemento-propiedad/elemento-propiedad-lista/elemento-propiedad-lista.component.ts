import { Router } from '@angular/router';
import { TipoEstado } from 'src/app/enums';
import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ElementoPropiedad } from '../elemento-propiedad';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ElementoPropiedadService } from '../elemento-propiedad.service';
import { Component, OnInit, Input, ViewChild, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { EncabezadoComponent } from 'src/app/encabezado-app/encabezado/encabezado.component';
import { ElementoPropiedadCrearComponent } from './elemento-propiedad-crear/elemento-propiedad-crear.component';
import { ElementoPropiedadEditarComponent } from './elemento-propiedad-editar/elemento-propiedad-editar.component';

@Component({
  standalone: true,
  selector: 'app-elemento-propiedad-lista',
  styleUrl: './elemento-propiedad-lista.component.css',
  templateUrl: './elemento-propiedad-lista.component.html',
  imports: [CommonModule, ReactiveFormsModule, EncabezadoComponent, ElementoPropiedadCrearComponent, ElementoPropiedadEditarComponent],
})

export class ElementoPropiedadListaComponent implements OnInit {
  idPropiedad!: number;
  nombreElementoReciente: string = '';
  elementos: Array<ElementoPropiedad> = [];
  elementoSeleccionado: ElementoPropiedad | null = null;

  @ViewChild('modalExito') modalExito!: TemplateRef<any>;
  @ViewChild('modalConfirmarEliminar') modalConfirmarEliminar!: TemplateRef<any>;
  @ViewChild('modalEliminarConfirmado') modalEliminarConfirmadoTemplate!: TemplateRef<any>;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private modalService: NgbModal,
    private elementoService: ElementoPropiedadService,
  ) { }

  ngOnInit(): void {
    // Obtenemos el ID de la propiedad desde la URL (/propiedades/1/elementos)
    this.idPropiedad = Number(this.route.snapshot.paramMap.get('id'));
    this.cargarElementos();
  }

  cargarElementos(): void {
    this.elementoService.darElementosPropiedad(this.idPropiedad).subscribe({
      next: (res) => {
        this.elementos = res;
        if (this.elementoSeleccionado) {
          this.elementoSeleccionado = this.elementos.find(e => e.id === this.elementoSeleccionado!.id) ?? null;
        }
      },
      error: () => this.toastr.error("Error al cargar inventario")
    });
  }

  obtenerElementos() {
    this.elementoService.darElementosPropiedad(this.idPropiedad).subscribe({
      next: (res) => {
        this.elementos = res;
        if (this.elementoSeleccionado) {
          this.elementoSeleccionado = this.elementos.find(e => e.id === this.elementoSeleccionado!.id) ?? null;
        }
      },
      error: (err) => this.toastr.error(`Error {${err.statusText}} al cargar la lista`)
    });
  }

  seleccionarElemento(elemento: ElementoPropiedad): void {
    this.elementoSeleccionado = elemento;
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

  modalAvisoEliminado(nombre: string) {
    
    // Guardamos el nombre del elemento recién creado
    this.nombreElementoReciente = nombre;
    
    // Presentación del modal
    const modalRef = this.modalService.open(this.modalEliminarConfirmadoTemplate, { centered: true, size: 'sm' });
    
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
  
  abrirModalCrear() {
    // Abrir modal
    const modalRef = this.modalService.open(ElementoPropiedadCrearComponent, { size: 'lg', centered: true });
    
    // Solo pasamos el ID de la propiedad, NO pasamos elementoExistente
    modalRef.componentInstance.idPropiedad = this.idPropiedad;

    // Recargar lista
    modalRef.result.then((result) => {
      if (result) { 
        this.obtenerElementos(); 
      }
    }).catch(() => {});
  }

  abrirModalEditar(elemento: ElementoPropiedad) {
    // Abrir modal
    const modalRef = this.modalService.open(ElementoPropiedadEditarComponent, { size: 'lg', centered: true });

    // Pasamos el ID del propiedad desde la URL (/propiedades/1/elementos)
    modalRef.componentInstance.idPropiedad = this.idPropiedad;

    // Pasamos el objeto completo para que el formulario se llene
    modalRef.componentInstance.elementoExistente = elemento;

    // Recargar lista
    modalRef.result.then((result) => {
      if (result) { 
        this.obtenerElementos();
      }
    }).catch(() => {});
  }

  eliminarElemento(elemento: ElementoPropiedad): void {
    // 1. Preparamos el nombre para el modal
    this.nombreElementoReciente = elemento.nombre;
    
    // 2. ABRIMOS el modal de confirmación que creaste en el HTML
    const modalRef = this.modalService.open(this.modalConfirmarEliminar, { centered: true, size: 'sm' });

    // 3. Escuchamos la respuesta del modal
    modalRef.result.then((result) => {
      if (result === 'confirmar') {
        // Si el usuario confirmó, llamamos al servicio
        this.elementoService.borrarElementoPropiedad(this.idPropiedad, elemento.id).subscribe({
          next: () => {
            this.toastr.success("Elemento eliminado correctamente");
            this.elementoSeleccionado = null;
            this.obtenerElementos();
            this.modalAvisoEliminado(elemento.nombre);
          },
          error: () => this.toastr.error("Error al eliminar el elemento")
        });
      }
    }).catch(() => {
      // En caso de cancelar, no se aplicaran cambios
    });
  }
}
