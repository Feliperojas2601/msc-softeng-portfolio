// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { NuevaAlarmaService, DiaChip } from '../services/nueva-alarma.service';

/**
 * NuevaPage
 *
 * Maqueta navegable (NO funcional) del paso 1/3 de creación de una alarma:
 * hora, días y etiqueta. Nodo de Figma 11:58 "M02-nueva".
 */
@Component({
  selector: 'app-nueva',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, IonContent],
  templateUrl: './nueva.page.html',
  styleUrl: './nueva.page.scss',
})
export class NuevaPage {

  // Constructor
  constructor(
    private readonly router: Router,
    protected readonly alarma: NuevaAlarmaService,
  ) {}

  // Alternar un día
  protected toggleDia(dia: DiaChip): void {
    this.alarma.toggleDia(dia);
  }

  // Continuar al paso 2/3
  protected onContinuar(): void {
    this.router.navigate(['/snooze']);
  }
}
