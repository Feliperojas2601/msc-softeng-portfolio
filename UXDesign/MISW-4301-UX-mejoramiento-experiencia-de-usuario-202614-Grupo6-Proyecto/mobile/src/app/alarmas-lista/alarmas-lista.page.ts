// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';

// Tipo de una alarma en la lista
interface AlarmaItem {
  etiqueta: string;
  hora: string;
  dias: string;
  reto: string;
  activa: boolean;
}

/**
 * AlarmasListaPage
 *
 * Maqueta navegable (NO funcional) de la lista de alarmas ya poblada.
 * Nodo de Figma 10:50 "M02-alarmas-lista".
 */
@Component({
  selector: 'app-alarmas-lista',
  standalone: true,
  imports: [CommonModule, RouterLink, IonContent],
  templateUrl: './alarmas-lista.page.html',
  styleUrl: './alarmas-lista.page.scss',
})
export class AlarmasListaPage {

  // Alarmas mock
  protected readonly alarmas: AlarmaItem[] = [
    { etiqueta: 'Gym · 06:30 · Lun–Vie', hora: '06:30', dias: 'Lun–Vie', reto: 'Reto: caminar 40 pasos', activa: true },
    { etiqueta: 'Trote · 08:00 · Sáb–Dom', hora: '08:00', dias: 'Sáb–Dom', reto: 'Reto: caminar 20 pasos', activa: true },
  ];

  // Constructor
  constructor(private readonly router: Router) {}

  // Alternar el estado de una alarma
  protected toggleAlarma(alarma: AlarmaItem): void {
    alarma.activa = !alarma.activa;
  }

  // Simular que una alarma está sonando y entrar al reto activo
  protected onSimularAlarmaSonando(): void {
    this.router.navigate(['/reto-curso']);
  }
}
