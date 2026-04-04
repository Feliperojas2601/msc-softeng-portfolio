import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MovimientoEditarComponent } from './movimiento-editar.component';

@NgModule({
  imports: [CommonModule, MovimientoEditarComponent],
  exports: [MovimientoEditarComponent],
})
export class MovimientoEditarModule { }
