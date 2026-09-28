// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { NuevaAlarmaService } from '../services/nueva-alarma.service';

/**
 * RetoConfigPage
 *
 * Maqueta navegable (NO funcional) del paso 3/3 de creación de una alarma:
 * pasos a caminar para el reto de movimiento. Nodo de Figma 11:182
 * "M02-reto-config".
 */
@Component({
  selector: 'app-reto-config',
  standalone: true,
  imports: [CommonModule, RouterLink, IonContent],
  templateUrl: './reto-config.page.html',
  styleUrl: './reto-config.page.scss',
})
export class RetoConfigPage {

  // Constructor
  constructor(
    private readonly router: Router,
    protected readonly alarma: NuevaAlarmaService,
  ) {}

  // Ajustar los pasos a caminar
  protected ajustarPasos(delta: number): void {
    this.alarma.ajustarPasosCaminar(delta);
  }

  // Guardar la alarma y volver a la lista
  protected onGuardar(): void {
    this.alarma.reset();
    this.router.navigate(['/alarmas-lista']);
  }
}
