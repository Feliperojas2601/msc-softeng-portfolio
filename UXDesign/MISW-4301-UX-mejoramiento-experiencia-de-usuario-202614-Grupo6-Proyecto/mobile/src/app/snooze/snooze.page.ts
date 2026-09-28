// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { NuevaAlarmaService } from '../services/nueva-alarma.service';

/**
 * SnoozePage
 *
 * Maqueta navegable (NO funcional) del paso 2/3 de creación de una alarma:
 * duración del reto y límite de posposiciones. Nodo de Figma 11:130
 * "M02-snooze".
 */
@Component({
  selector: 'app-snooze',
  standalone: true,
  imports: [CommonModule, RouterLink, IonContent],
  templateUrl: './snooze.page.html',
  styleUrl: './snooze.page.scss',
})
export class SnoozePage {

  // Constructor
  constructor(
    private readonly router: Router,
    protected readonly alarma: NuevaAlarmaService,
  ) {}

  // Seleccionar una duración
  protected seleccionarDuracion(duracion: string): void {
    this.alarma.duracionSeleccionada = duracion;
  }

  // Ajustar el límite de posposiciones
  protected ajustarLimite(delta: number): void {
    this.alarma.ajustarLimitePosposiciones(delta);
  }

  // Continuar al paso 3/3
  protected onContinuar(): void {
    this.router.navigate(['/reto-config']);
  }
}
