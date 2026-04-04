import { forkJoin } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { Movimiento } from '../movimiento';
import { TipoMovimiento } from 'src/app/enums';
import { CommonModule } from '@angular/common';
import { Reserva } from 'src/app/reserva/reserva';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { Categoria } from 'src/app/categoria/categoria';
import { Component, OnInit, Input } from '@angular/core';
import { MovimientoService } from '../movimiento.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ReservaService } from 'src/app/reserva/reserva.service';
import { CategoriaService } from 'src/app/categoria/categoria.service';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CategoriaSelectorComponent } from 'src/app/categoria/categoria-selector/categoria-selector.component';

@Component({
  standalone: true,
  selector: 'app-movimiento-editar',
  imports: [CommonModule, ReactiveFormsModule, CategoriaSelectorComponent],
  templateUrl: './movimiento-editar.component.html',
  styleUrls: ['./movimiento-editar.component.css']
})
export class MovimientoEditarComponent implements OnInit {

  // Recibimos el id de la propiedad para la cual se va a crear el movimiento y el id del movimiento a editar
  @Input() idMovimiento!: number;
  @Input() idPropiedad!: number;

  // Definimos las variables necesarias para el componente
  movimiento!: Movimiento;
  movimientoForm: FormGroup;
  listaReservas: Array<Reserva> = [];
  tiposMovimiento: Array<TipoMovimiento> = [];
  listaCategorias: Array<Categoria> = [];

  // Constructor
  constructor(    
    // Importamos las dependencias necesarias para el componente
    private toastr: ToastrService,
    private formBuilder: FormBuilder,
    private enumService: EnumsService,
    private errorService: ErrorService,
    private activeModal: NgbActiveModal,
    private reservaService: ReservaService,
    private categoriaService: CategoriaService,
    private movimientoService: MovimientoService,
  ) {
    this.movimientoForm = this.formBuilder.group({
      fecha: ["", Validators.required],
      concepto: ["", Validators.required],
      valor: ["", Validators.required],
      tipo_movimiento: ["", Validators.required],
      id_categoria: ["", Validators.required],
      id_reserva: [null, []]
    });
   }

  ngOnInit() {
    
    // Obtenemos el id del movimiento a editar
    this.movimientoService.obtenerMovimiento(this.idMovimiento).subscribe({
      next: (movimiento) => {
        // Si la petición es exitosa, obtenemos el movimiento a editar
        this.movimiento = movimiento;

        forkJoin({
          // Obtenemos la lista de reservas, tipos de movimiento y categorías
          reservas: this.reservaService.obtenerReservas(this.idPropiedad),
          tiposMovimiento: this.enumService.tiposMovimiento(),
          categorias: this.categoriaService.darCategorias()

        }).subscribe({
          next: ({ reservas, tiposMovimiento, categorias }) => {
            
            // Si la petición es exitosa, obtenemos la lista de reservas, tipos de movimiento y categorías, y llenamos el formulario con los datos del movimiento a editar
            this.listaReservas = reservas;
            this.tiposMovimiento = tiposMovimiento;
            this.listaCategorias = categorias;

            // Si la petición es exitosa, actualizamos el formulario con los datos del movimiento a editar
            this.movimientoForm.patchValue({
              fecha: this.movimiento.fecha,
              concepto: this.movimiento.concepto,
              valor: this.movimiento.valor,
              tipo_movimiento: this.movimiento.tipo_movimiento,
              id_categoria: this.movimiento.id_categoria,
              id_reserva: this.movimiento.id_reserva
            });
          },
          // Si la petición falla, mostramos un mensaje de error y manejamos el error
          error: (error) => this.errorService.manejarError(error)
        });
      },
      error: (error) => this.errorService.manejarError(error)
    });
  }

  editar(): void {
    
    // Validamos el formulario
    if (this.movimientoForm.invalid) {
      this.movimientoForm.markAllAsTouched();
      return;
    }

    // Si el formulario es válido, actualizamos el movimiento con los datos del formulario
    this.movimientoService.actualizarMovimiento(this.movimientoForm.value, this.movimiento.id).subscribe({
      
      // Mensaje de éxito al actualizar el movimiento
      next: () => {
        this.toastr.success("Movimiento actualizado correctamente");
        this.activeModal.close(true);  
      },
      // Mensaje de error al actualizar el movimiento
      error: (error) => {
        this.toastr.error("Error al actualizar el movimiento");
        this.errorService.manejarError(error);
      }
    });
  }

  cancelar(): void {
    // Cierra el modal sin recargar la lista
    this.activeModal.dismiss();
  }
}
