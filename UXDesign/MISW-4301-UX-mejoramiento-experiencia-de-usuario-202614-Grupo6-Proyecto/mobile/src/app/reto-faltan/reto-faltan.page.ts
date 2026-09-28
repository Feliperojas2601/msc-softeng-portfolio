// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { RetoService } from '../services/reto.service';

/**
 * RetoFaltanPage
 *
 * Maqueta navegable (NO funcional). Nodo de Figma 14:63 "M03-reto-faltan".
 * Muestra el estado "aún faltan pasos" con el banner de aviso.
 */

// Componente
@Component({
  selector: 'app-reto-faltan',
  standalone: true,
  imports: [CommonModule, RouterLink, IonContent],
  templateUrl: './reto-faltan.page.html',
  styleUrl: './reto-faltan.page.scss',
})
export class RetoFaltanPage {

  // Constructor
  constructor(
    private readonly router: Router,
    private readonly retoService: RetoService
  ) {}

  // Limpiar el foco activo
  private clearActiveFocus(): void {
    const activeElement = document.activeElement;

    if (activeElement instanceof HTMLElement) {
      activeElement.blur();
    }
  }

  // Variables de estado
  protected get totalSteps(): number {
    return this.retoService.totalSteps;
  }

  // Obtener los pasos actuales
  protected get currentSteps(): number {
    return this.retoService.currentSteps;
  }

  // Obtener los pasos faltantes
  protected get missingSteps(): number {
    return this.retoService.missingSteps;
  }

  // Métodos de cálculo de estado
  protected get progressPercent(): number {
    return this.retoService.progressPercent;
  }

  // Métodos de cálculo de estilo
  protected get ringGradient(): string {
    
    // Porcentaje de progreso
    const p = this.progressPercent;

    // Retorno del gradiente
    return `conic-gradient(
      #E68A3E 0% ${p}%,
      #D9CFC0 ${p}% 100%
    )`;
  }

  // Continuar con el reto
  protected onTapSimulate(): void {
    const state = this.retoService.advanceSteps();

    if (state === 'completed') {
      this.clearActiveFocus();

      requestAnimationFrame(() => {
        this.router.navigate(['/reto-ok']);
      });
    }
  }
}