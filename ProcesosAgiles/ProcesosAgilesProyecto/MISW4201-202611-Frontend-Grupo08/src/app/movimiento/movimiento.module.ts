import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MovimientoListaComponent } from './movimiento-lista/movimiento-lista.component';
import { MovimientoEditarComponent } from './movimiento-editar/movimiento-editar.component';
import { MovimientoCrearComponent } from './movimiento-crear/movimiento-crear.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MovimientoListaComponent,
    MovimientoEditarComponent,
    MovimientoCrearComponent,
  ],
  exports: [
    MovimientoListaComponent,
    MovimientoEditarComponent,
    MovimientoCrearComponent,
  ]
})
export class MovimientoModule { }
