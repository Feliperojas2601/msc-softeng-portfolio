// Libraries
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatSidenavModule } from '@angular/material/sidenav';
import { ALARM_DAYS, ALARM_DATA, DISTRIBUTION, RESPONSE_TIME, RECENT_HISTORY, CURRENT_USER, } from './mock-data';

/**
 * DetalleAlarmaComponent
 *
 * Maqueta navegable (NO funcional) del detalle de una alarma
 * (nodo de Figma 121:107 "W02-detalle-alarma"). Datos mock,
 * sin llamadas HTTP ni estado real.
 */
@Component({
  selector: 'app-detalle-alarma',
  standalone: true,
  imports: [CommonModule, RouterLink, MatSidenavModule],
  templateUrl: './detalle-alarma.html',
  styleUrl: './detalle-alarma.scss',
})
export class DetalleAlarmaComponent {
  protected readonly user = CURRENT_USER;
  protected readonly alarmName = 'Gym';
  protected readonly alarmTime = '06:30';
  protected readonly alarmDays = ALARM_DAYS;
  protected readonly alarmData = ALARM_DATA;
  protected readonly distribution = DISTRIBUTION;
  protected readonly responseTime = RESPONSE_TIME;
  protected readonly recentHistory = RECENT_HISTORY;
  
  // Gradiente de color de la dona (con el color de la paleta de colores
  protected get donaGradient(): string {  
    
    // El porcentaje de cada color en la dona es fijo, no depende de los datos
    const exitoPct = 68;
    const acentoPct = exitoPct + 22;

    // El gradiente es un conic, con los dos colores de la paleta de colores
    return `conic-gradient( #6E9C7E 0% ${exitoPct}%, #E68A3E ${exitoPct}% ${acentoPct}%, #C0523F ${acentoPct}% 100% )`;
  }
}

