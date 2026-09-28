// Libraries
import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { PerfilComponent } from './perfil/perfil';
import { DashboardComponent } from './dashboard/dashboard';
import { DetalleAlarmaComponent } from './detalle-alarma/detalle-alarma';
import { RetoEscrituraComponent } from './reto-escritura/reto-escritura';
import { RetoCompletadoComponent } from './reto-completado/reto-completado';
import { DetalleAlarmaVivoComponent } from './detalle-alarma-vivo/detalle-alarma-vivo';

// Routes
export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'alarma/:id', component: DetalleAlarmaComponent },
  { path: 'alarma/:id/vivo', component: DetalleAlarmaVivoComponent },
  { path: 'perfil', component: PerfilComponent },
  { path: 'reto-escritura', component: RetoEscrituraComponent },
  { path: 'reto-completado', component: RetoCompletadoComponent },
];
