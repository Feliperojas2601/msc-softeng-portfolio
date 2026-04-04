import { forkJoin } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { Movimiento } from '../movimiento';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ErrorService } from 'src/app/error.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { MovimientoService } from '../movimiento.service';
import { CategoriaService } from 'src/app/categoria/categoria.service';
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { MovimientoCrearComponent } from '../movimiento-crear/movimiento-crear.component';
import { EncabezadoComponent } from '../../encabezado-app/encabezado/encabezado.component';
import { MovimientoEditarComponent } from '../movimiento-editar/movimiento-editar.component';

@Component({
  standalone: true,
  selector: 'app-movimiento-lista',
  imports: [CommonModule, EncabezadoComponent, MovimientoEditarComponent],
  templateUrl: './movimiento-lista.component.html',
  styleUrls: ['./movimiento-lista.component.css']
})
export class MovimientoListaComponent implements OnInit {

  idPropiedad: number;
  totalEgresos: number           = 0;
  totalIngresos: number          = 0;
  movimientos: Array<Movimiento> = [];
  egresos: Array<Movimiento>     = [];
  ingresos: Array<Movimiento>    = [];
  categoriaMap: Map<number, string> = new Map();
  movimientoSeleccionado: Movimiento | null = null;

  constructor(
    private toastr: ToastrService,
    private modalService: NgbModal,
    private router: ActivatedRoute,
    private errorService: ErrorService,
    private cdr: ChangeDetectorRef,
    private movimientoService: MovimientoService,
    private categoriaService: CategoriaService
  ) { }

  ngOnInit() {
    this.idPropiedad = parseInt(this.router.snapshot.params['id']);
    this.cargarTodo();
  }

  // Método central que carga categorías y movimientos juntos
  cargarTodo(idMovimientoSeleccionado?: number): void {
    forkJoin({
      categorias: this.categoriaService.darCategorias(),
      movimientos: this.movimientoService.obtenerMovimientos(this.idPropiedad)
    }).subscribe({
      next: ({ categorias, movimientos }) => {
        this.categoriaMap  = new Map(categorias.map(c => [c.id, c.nombre]));
        this.movimientos   = movimientos;
        this.ingresos      = movimientos.filter(m => m.tipo_movimiento === 'INGRESO');
        this.egresos       = movimientos.filter(m => m.tipo_movimiento === 'EGRESO');
        this.totalIngresos = this.ingresos.reduce((sum, m) => sum + m.valor, 0);
        this.totalEgresos  = this.egresos.reduce((sum, m)  => sum + m.valor, 0);

        // Si viene un id, actualizamos el movimiento seleccionado con el objeto fresco
        if (idMovimientoSeleccionado) {
          this.movimientoSeleccionado = movimientos.find(m => m.id === idMovimientoSeleccionado) ?? null;
        }

        this.cdr.detectChanges();
      },
      error: (error) => this.errorService.manejarError(error)
    });
  }

  nombreCategoria(idCategoria: number): string {
    return this.categoriaMap.get(idCategoria) ?? '—';
  }

  seleccionarMovimiento(movimiento: Movimiento): void {
    this.movimientoSeleccionado = movimiento;
  }

  crearMovimiento(): void {
    const modalRef = this.modalService.open(MovimientoCrearComponent, {
      size: 'lg',
      centered: true
    });
    modalRef.componentInstance.idPropiedad = this.idPropiedad;
    modalRef.result.then((result) => {
      if (result) this.cargarTodo();
    }).catch(() => {});
  }

  editarMovimiento(idMovimiento: number): void {
    const modalRef = this.modalService.open(MovimientoEditarComponent, {
      size: 'lg',
      centered: true
    });
    modalRef.componentInstance.idMovimiento = idMovimiento;
    modalRef.componentInstance.idPropiedad  = this.idPropiedad;
    modalRef.result.then((result) => {
      if (result) this.cargarTodo(idMovimiento); // ← pasa el id para re-seleccionar
    }).catch(() => {});
  }

  borrarMovimiento(idMovimiento: number): void {
    this.movimientoService.eliminarMovimiento(idMovimiento).subscribe({
      next: () => {
        this.toastr.success("Movimiento eliminado correctamente");
        if (this.movimientoSeleccionado?.id === idMovimiento) {
          this.movimientoSeleccionado = null;
        }
        this.cargarTodo();
      },
      error: (error) => this.errorService.manejarError(error)
    });
  }
}