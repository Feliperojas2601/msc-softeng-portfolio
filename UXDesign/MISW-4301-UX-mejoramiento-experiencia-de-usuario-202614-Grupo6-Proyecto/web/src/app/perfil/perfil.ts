// Libraries
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatSidenavModule } from '@angular/material/sidenav';

// Mock data PreferenceRow
export interface PreferenceRow {
  label: string;
  description: string;
  active: boolean;
}

// Mock data EmergencyExit
export interface EmergencyExit {
  title: string;
  subtitle: string;
}

/**
 * PerfilComponent
 *
 * Maqueta navegable (NO funcional). Nodo de Figma 116:137 "W01-perfil".
 * El sidebar y la barra superior reutilizan exactamente la misma
 * estructura/clases ya usadas en DetalleAlarmaComponent — nada nuevo ahí.
 */
@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, RouterLink, MatSidenavModule],
  templateUrl: './perfil.html',
  styleUrl: './perfil.scss',
})
export class PerfilComponent {
  
  // Mock data user
  protected readonly user = {
    initials: 'PA',
    name: 'Paula Alarcón',
    email: 'paula.abc@gmail.com',
  };

  // Mock data Member since
  protected readonly memberSince = 'Cuenta activa desde marzo de 2026 · 2 dispositivos sincronizados';

  // Mock data Preferences
  protected readonly preferences: PreferenceRow[] = [
    {
      label: 'Sincronizar con el móvil',
      description: 'Tus alarmas se reflejan en ambos dispositivos.',
      active: true,
    },
    {
      label: 'Sonido de alarma en el navegador',
      description: 'Suena aunque la pestaña esté en segundo plano.',
      active: true,
    },
    {
      label: 'Recordatorio nocturno',
      description: 'Te avisamos 30 min antes de tu hora de dormir.',
      active: false,
    },
  ];

  // Mock data Emergency Count
  protected readonly emergencyCount = 2;

  // Mock data Emergency Exits
  protected readonly emergencyExits: EmergencyExit[] = [
    { title: 'Ayer · 06:34', subtitle: 'Gym · Reto de escritura' },
    { title: '12 sep · 06:31', subtitle: 'Gym · Reto de escritura' },
  ];
}
