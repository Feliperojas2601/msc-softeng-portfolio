// Libraries
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatSidenavModule } from '@angular/material/sidenav';
import { ALARM_DAYS, ALARM_DATA, DISTRIBUTION, RESPONSE_TIME, CURRENT_USER,} from './mock-data';

/**
 * DetalleAlarmaVivoComponent
 *
 * Maqueta navegable (NO funcional) del detalle de una alarma que está
 * sonando en este momento (nodo de Figma 121:170 "W02-detalle-alarma-vivo").
 * Datos mock, sin llamadas HTTP ni estado real.
 */
@Component({
    selector: 'app-detalle-alarma-vivo',
    standalone: true,
    imports: [CommonModule, RouterLink, MatSidenavModule],
    templateUrl: './detalle-alarma-vivo.html',
    styleUrl: './detalle-alarma-vivo.scss',
})
// Mock data
export class DetalleAlarmaVivoComponent {
    protected readonly user = CURRENT_USER;
    protected readonly alarmName = 'Gym';
    protected readonly alarmTime = '06:30';
    protected readonly secondsSonando = 42;
    protected readonly posponerRestantes = 2;
    protected readonly alarmDays = ALARM_DAYS;
    protected readonly alarmData = ALARM_DATA;
    protected readonly distribution = DISTRIBUTION;
    protected readonly responseTime = RESPONSE_TIME;

    // Variables de estado
    protected get donaGradient(): string {
        const exitoPct = 68;
        const acentoPct = exitoPct + 22;
        return `conic-gradient( #6E9C7E 0% ${exitoPct}%, #E68A3E ${exitoPct}% ${acentoPct}%, #C0523F ${acentoPct}% 100% )`;
    }
}
