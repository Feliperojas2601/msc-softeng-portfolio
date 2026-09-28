import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'alarmas-lista',
    pathMatch: 'full',
  },
  {
    path: 'alarmas-lista',
    loadComponent: () => import('./alarmas-lista/alarmas-lista.page').then( m => m.AlarmasListaPage)
  },
  {
    path: 'nueva',
    loadComponent: () => import('./nueva/nueva.page').then( m => m.NuevaPage)
  },
  {
    path: 'snooze',
    loadComponent: () => import('./snooze/snooze.page').then( m => m.SnoozePage)
  },
  {
    path: 'reto-config',
    loadComponent: () => import('./reto-config/reto-config.page').then( m => m.RetoConfigPage)
  },
  {
    path: 'reto-curso',
    loadComponent: () => import('./reto-curso/reto-curso.page').then( m => m.RetoCursoPage)
  },
  {
    path: 'reto-faltan',
    loadComponent: () => import('./reto-faltan/reto-faltan.page').then( m => m.RetoFaltanPage)
  },
  {
    path: 'reto-ok',
    loadComponent: () => import('./reto-ok/reto-ok.page').then( m => m.RetoOkPage)
  },
];
