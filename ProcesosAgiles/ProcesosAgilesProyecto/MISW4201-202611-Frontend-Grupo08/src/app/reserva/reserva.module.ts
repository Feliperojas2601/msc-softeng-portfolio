import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { EncabezadoAppModule } from '../encabezado-app/encabezado-app.module';
import { ReservaListaComponent } from './reserva-lista/reserva-lista.component';
import { ReservaCrearComponent } from './reserva-crear/reserva-crear.component';
import { ReservaEditarComponent } from './reserva-editar/reserva-editar.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    EncabezadoAppModule
  ],
  declarations: [
    ReservaListaComponent,
    ReservaCrearComponent,
    ReservaEditarComponent
  ],
  exports: [
    ReservaListaComponent,
    ReservaCrearComponent,
    ReservaEditarComponent
  ]
})
export class ReservaModule { }
