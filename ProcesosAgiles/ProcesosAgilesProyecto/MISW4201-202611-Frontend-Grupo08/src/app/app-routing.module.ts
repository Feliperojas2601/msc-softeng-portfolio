import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UsuarioLoginComponent } from './usuario/usuario-login/usuario-login.component';
import { UsuarioRegistroComponent } from './usuario/usuario-registro/usuario-registro.component';
import { PropiedadListaComponent } from './propiedad/propiedad-lista/propiedad-lista.component';
import { PropiedadCrearComponent } from './propiedad/propiedad-crear/propiedad-crear.component';
import { PropiedadEditarComponent } from './propiedad/propiedad-editar/propiedad-editar.component';
import { ReservaListaComponent } from './reserva/reserva-lista/reserva-lista.component';
import { ReservaCrearComponent } from './reserva/reserva-crear/reserva-crear.component';
import { ReservaEditarComponent } from './reserva/reserva-editar/reserva-editar.component';
import { MovimientoListaComponent } from './movimiento/movimiento-lista/movimiento-lista.component';
import { MovimientoEditarComponent } from './movimiento/movimiento-editar/movimiento-editar.component';
import { MovimientoCrearComponent } from './movimiento/movimiento-crear/movimiento-crear.component';

const routes: Routes = [
  { path: '', component: UsuarioLoginComponent, pathMatch: 'full' },
  { path: 'registro', component: UsuarioRegistroComponent,  pathMatch: 'full' },
  { path: 'propiedades', component: PropiedadListaComponent, pathMatch: 'full'},
  { path: 'propiedad/crear', component: PropiedadCrearComponent, pathMatch: 'full'},
  { path: 'propiedad/editar/:id', component: PropiedadEditarComponent, pathMatch: 'full'},
  { path: 'propiedades/:id/reservas', component: ReservaListaComponent, pathMatch: 'full'},
  { path: 'propiedades/:id/movimientos', component: MovimientoListaComponent, pathMatch: 'full'},
  { path: 'propiedades/:id/movimientos/editar/:id_movimiento', component: MovimientoEditarComponent, pathMatch: 'full'},
  { path: 'propiedades/:id/movimientos/crear', component: MovimientoCrearComponent, pathMatch: 'full'},
  { path: 'propiedades/:id/reserva/crear', component: ReservaCrearComponent, pathMatch: 'full'},
  { path: 'propiedades/:id_propiedad/reserva/editar/:id_reserva', component: ReservaEditarComponent, pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
