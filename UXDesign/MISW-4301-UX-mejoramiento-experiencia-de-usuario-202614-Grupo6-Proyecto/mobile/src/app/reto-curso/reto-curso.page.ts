// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { RetoService } from '../services/reto.service';

/**
 * RetoCursoPage
 *
 * Maqueta navegable (NO funcional salvo por la simulación explícita que pide
 * el propio diseño: "toca la pantalla para simular que completas los pasos").
 * Nodo de Figma 14:35 "M03-reto-curso".
 */
@Component({
  selector: 'app-reto-curso',
  standalone: true,
  imports: [CommonModule, RouterLink, IonContent],
  templateUrl: './reto-curso.page.html',
  styleUrl: './reto-curso.page.scss',
})
export class RetoCursoPage {

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

  // Obtener el total de pasos
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

  // Obtener si se muestra el aviso de falta de pasos
  protected get showMissingNotice(): boolean {
    return this.currentSteps >= 32 && this.currentSteps < this.totalSteps;
  }

  // Métodos de cálculo de estado
  protected get progressPercent(): number {
    return this.retoService.progressPercent;
  }

  // Métodos de cálculo de estilo
  protected get ringGradient(): string {
    const p = this.progressPercent;

    return `conic-gradient(
      #E68A3E 0% ${p}%,
      #D9CFC0 ${p}% 100%
    )`;
  }

  /**
   * Simula el avance del usuario.
   * Al llegar a 32 pasos muestra el aviso.
   * Al llegar a 40 pasos finaliza el reto.
   */
  protected onTapSimulate(): void {

    // Avanzar pasos
    const state = this.retoService.advanceSteps();

    // Reto faltante
    if (state === 'missing') {
      this.clearActiveFocus();
      this.router.navigate(['/reto-faltan']);
      return;
    }

    // Reto completado
    if (state === 'completed') {
      this.clearActiveFocus();
      this.router.navigate(['/reto-ok']);
    }
  }
}