// Libraries
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

/**
 * RetoCompletadoComponent
 *
 * Maqueta navegable (NO funcional) de la pantalla de éxito que se muestra
 * al completar el reto de escritura (nodo de Figma 227:464
 * "W03-reto-completado"). Solo ofrece volver al dashboard.
 */
@Component({
    selector: 'app-reto-completado',
    standalone: true,
    imports: [RouterLink],
    templateUrl: './reto-completado.html',
    styleUrl: './reto-completado.scss',
})
export class RetoCompletadoComponent {}
