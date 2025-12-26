import { Component, EventEmitter, Input, Output, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';

export interface AssociationItem {
    id: string;
    name: string;
    photo?: string;
}

@Component({
    selector: 'app-association-modal',
    imports: [CommonModule, FormsModule],
    templateUrl: './association-modal.component.html',
    styleUrl: './association-modal.component.css',
})
export class AssociationModalComponent {
    @Input() title: string = 'Agregar';
    @Input() items: AssociationItem[] = [];
    @Input() isVisible: boolean = false;
    @Input() successMessage: string = 'Elemento agregado exitosamente';
    @Input() errorMessage: string = 'Error al agregar el elemento';
    @Output() onClose = new EventEmitter<void>();
    @Output() onSelect = new EventEmitter<string>();

    private readonly toastr = inject(ToastrService);
    public readonly isSubmitting = signal<boolean>(false);

    selectedItemId: string | null = null;

    close() {
        this.selectedItemId = null;
        this.onClose.emit();
    }

    selectItem(itemId: string) {
        this.selectedItemId = itemId;
    }

    confirm() {
        if (this.selectedItemId) {
            this.isSubmitting.set(true);
            this.onSelect.emit(this.selectedItemId);
        }
    }

    handleSuccess() {
        this.toastr.success(this.successMessage, 'Éxito', {
            closeButton: true,
        });
        this.isSubmitting.set(false);
        this.selectedItemId = null;
        this.onClose.emit();
    }

    handleError() {
        this.toastr.error(this.errorMessage, 'Error', {
            closeButton: true,
        });
        this.isSubmitting.set(false);
    }
}
