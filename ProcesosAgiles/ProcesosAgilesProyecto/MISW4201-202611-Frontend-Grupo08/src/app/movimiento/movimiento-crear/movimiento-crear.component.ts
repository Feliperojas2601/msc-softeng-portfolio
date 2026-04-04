import { forkJoin } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { TipoMovimiento } from 'src/app/enums';
import { CommonModule } from '@angular/common';
import { Reserva } from 'src/app/reserva/reserva';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { Categoria } from 'src/app/categoria/categoria';
import { Component, OnInit, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { MovimientoService } from '../movimiento.service';
import { ReservaService } from 'src/app/reserva/reserva.service';
import { CategoriaService } from 'src/app/categoria/categoria.service';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CategoriaSelectorComponent } from 'src/app/categoria/categoria-selector/categoria-selector.component';

@Component({
  standalone: true,
  selector: 'app-movimiento-crear',
  imports: [CommonModule, ReactiveFormsModule, CategoriaSelectorComponent],
  templateUrl: './movimiento-crear.component.html',
  styleUrls: ['./movimiento-crear.component.css']
})
export class MovimientoCrearComponent implements OnInit {

  // Recibimos el id de la propiedad para la cual se va a crear el movimiento
  @Input() idPropiedad!: number;

  // Formulario para crear el movimiento
  movimientoForm: FormGroup;
  listaReservas: Array<Reserva> = [];
  tiposMovimiento: Array<TipoMovimiento> = [];
  listaCategorias: Array<Categoria> = [];

  // Constructor
  constructor(
    private formBuilder: FormBuilder,
    private toastr: ToastrService,
    private enumService: EnumsService,
    private movimientoService: MovimientoService,
    private reservaService: ReservaService,
    private categoriaService: CategoriaService,
    private errorService: ErrorService,
    private activeModal: NgbActiveModal
  ) {
    
    // Creamos el formulario para crear el movimiento
    this.movimientoForm = this.formBuilder.group({
      fecha: ["", Validators.required],
      concepto: ["", Validators.required],
      valor: ["", Validators.required],
      id_reserva: [null, []],
      tipo_movimiento: [null, Validators.required],
      id_categoria: [null, Validators.required]
    });
  }

  ngOnInit() {
    // Obtenemos el id de la propiedad para la cual se va a crear el movimiento
    forkJoin({
      reservas: this.reservaService.obtenerReservas(this.idPropiedad),
      tiposMovimiento: this.enumService.tiposMovimiento(),
      categorias: this.categoriaService.darCategorias()
    }).subscribe({
      next: ({ reservas, tiposMovimiento, categorias }) => {
        this.listaReservas = reservas;
        this.tiposMovimiento = tiposMovimiento;
        this.listaCategorias = categorias;
      },
      error: (error) => this.errorService.manejarError(error)
    });
  }

  guardar(): void {

    // Validamos el formulario
    if (this.movimientoForm.invalid) {
      this.movimientoForm.markAllAsTouched();
      return;
    }

    // Creamos el movimiento
    this.movimientoService.crearMovimiento(this.movimientoForm.value, this.idPropiedad).subscribe({
      next: () => {
        this.toastr.success("Movimiento creado correctamente");
        this.activeModal.close(true);
      },
      // Si hay un error al crear el movimiento, mostramos un mensaje de error y manejamos el error
      error: (error) => {
        this.toastr.error("Error al crear el movimiento");
        this.errorService.manejarError(error);
      }
    });
  }

  cancelar() {
    this.activeModal.close(true);
  }

}
