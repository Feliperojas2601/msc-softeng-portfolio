// Librerías
import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

/**
 * RetoOkPage
 *
 * Maqueta navegable (NO funcional). Nodo de Figma 14:93 "M03-reto-ok".
 * Estado de reto completado (100%), con banner de éxito y botón para
 * cerrar la alarma.
 */
@Component({
  selector: 'app-reto-ok',
  standalone: true,
  imports: [CommonModule, RouterLink, IonContent],
  templateUrl: './reto-ok.page.html',
  styleUrl: './reto-ok.page.scss',
})

// Componente
export class RetoOkPage {
  protected readonly userName = 'Paula';
}
