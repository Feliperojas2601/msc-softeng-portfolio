// Libraries
import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

/**
 * RetoEscrituraComponent
 *
 * Maqueta navegable (NO funcional) de la pantalla en donde se escribe la
 * frase para apagar la alarma (nodo de Figma 121:236 "W03-reto-escritura").
 *
 * Incluye validación en vivo mientras se escribe (prevención de errores,
 * pedida por la monitora en un comentario de Figma): si lo escrito deja de
 * coincidir con la frase objetivo, el campo muestra un estado de error en
 * lugar de dejar avanzar en silencio.
 */
@Component({
    selector: 'app-reto-escritura',
    standalone: true,
    imports: [CommonModule, RouterLink, FormsModule],
    templateUrl: './reto-escritura.html',
    styleUrl: './reto-escritura.scss',
})

// Mock data
export class RetoEscrituraComponent {
    
    // Variables de estado
    protected readonly targetPhrase = 'El sol ya salió, es hora de continuar';
    protected typedText = 'El sol ya salió, es hora de co';

    // Constructor
    constructor(private readonly router: Router) {}

    // Progress
    protected get progressPercent(): number {
        return Math.min(100, (this.typedText.length / this.targetPhrase.length) * 100);
    }

    // Error state
    protected get hasError(): boolean {
        return this.typedText.length > 0 && !this.targetPhrase.startsWith(this.typedText);
    }

    // Completion state
    protected get isComplete(): boolean {
        return this.typedText === this.targetPhrase;
    }

    // If challenge is complete, navigate to the "reto completado" page
    protected onTypedTextChange(): void {
        if (this.isComplete) {
            this.router.navigateByUrl('/reto-completado');
        }
    }
}
