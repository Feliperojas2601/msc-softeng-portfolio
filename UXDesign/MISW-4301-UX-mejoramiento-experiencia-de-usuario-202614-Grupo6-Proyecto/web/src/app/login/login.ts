// Libraries
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

/**
 * LoginComponent
 *
 * Maqueta navegable (NO funcional) de la pantalla de inicio de sesión
 * (nodo de Figma 116:101 "W01-login"). Los botones de Google/Apple solo
 * navegan al dashboard — no hay autenticación real.
 */
@Component({
    selector: 'app-login',
    standalone: true,
    imports: [RouterLink],
    templateUrl: './login.html',
    styleUrl: './login.scss',
})
export class LoginComponent {}
