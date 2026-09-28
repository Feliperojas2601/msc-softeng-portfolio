// Librerías
import { Injectable } from '@angular/core';

// Tipos de estado
export type RetoStepState = 'progress' | 'missing' | 'completed';

// Servicio de reto
@Injectable({ providedIn: 'root',})

// Clase
export class RetoService {

  // Configuración del reto
  readonly totalSteps = 40;
  readonly stepIncrement = 4;

  // Estado actual
  currentSteps = 12;

  // Evita mostrar varias veces la pantalla "reto-faltan"
  private missingNoticeShown = false;

  // Incrementar pasos
  advanceSteps(): RetoStepState {

    // Reto completado
    if (this.currentSteps >= this.totalSteps) {
      return 'completed';
    }

    // Incrementar pasos
    this.currentSteps = Math.min(
      this.totalSteps,
      this.currentSteps + this.stepIncrement
    );

    // Mostrar aviso una sola vez al alcanzar los 32 pasos
    if ( this.currentSteps >= 32 && this.currentSteps < this.totalSteps && !this.missingNoticeShown ) {
      
      // Mostrar aviso
      this.missingNoticeShown = true;

      // Reto faltantes
      return 'missing';
    }

    // Reto completado
    if (this.currentSteps >= this.totalSteps) {
      
      // Reto completado
      return 'completed';
    }
    
    // Reto en progreso
    return 'progress';
  }

  // Pasos faltantes
  get missingSteps(): number {
    return this.totalSteps - this.currentSteps;
  }

  // Porcentaje de progreso
  get progressPercent(): number {
    return Math.round( (this.currentSteps / this.totalSteps) * 100 );
  }

  // Reiniciar el reto
  reset(): void {
    this.currentSteps = 12;
    this.missingNoticeShown = false;
  }
}