// Librerías
import { Injectable } from '@angular/core';

// Días de la semana disponibles para una alarma
export interface DiaChip {
  label: string;
  active: boolean;
}

// Servicio del asistente de creación de alarma (3 pasos)
@Injectable({ providedIn: 'root' })

// Clase
export class NuevaAlarmaService {

  // Paso 1 — Nueva alarma
  hora = '06:00 AM';
  etiqueta = 'Gym';
  dias: DiaChip[] = [
    { label: 'L', active: true },
    { label: 'M', active: true },
    { label: 'X', active: true },
    { label: 'J', active: true },
    { label: 'V', active: true },
    { label: 'S', active: false },
    { label: 'D', active: false },
  ];

  // Paso 2 — Snooze
  readonly duraciones = ['5 min', '10 min', '15 min'];
  duracionSeleccionada = '5 min';
  limitePosposiciones = 3;

  // Paso 3 — Reto de movimiento
  pasosCaminar = 40;

  // Alternar un día seleccionado
  toggleDia(dia: DiaChip): void {
    dia.active = !dia.active;
  }

  // Ajustar el límite de posposiciones (0 a 5)
  ajustarLimitePosposiciones(delta: number): void {
    this.limitePosposiciones = Math.min(5, Math.max(0, this.limitePosposiciones + delta));
  }

  // Ajustar los pasos a caminar (10 a 100, de 5 en 5)
  ajustarPasosCaminar(delta: number): void {
    this.pasosCaminar = Math.min(100, Math.max(10, this.pasosCaminar + delta));
  }

  // Reiniciar el asistente a sus valores por defecto
  reset(): void {
    this.hora = '06:00 AM';
    this.etiqueta = 'Gym';
    this.dias.forEach((d) => (d.active = ['L', 'M', 'X', 'J', 'V'].includes(d.label)));
    this.duracionSeleccionada = '5 min';
    this.limitePosposiciones = 3;
    this.pasosCaminar = 40;
  }
}
