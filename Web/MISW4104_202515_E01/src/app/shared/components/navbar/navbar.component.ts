import {
    ChangeDetectionStrategy,
    Component,
    inject,
    signal,
} from '@angular/core';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-navbar',
    imports: [CommonModule, RouterLink, RouterLinkActive],
    templateUrl: './navbar.component.html',
    styleUrls: ['./navbar.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NavbarComponent {
    private router = inject(Router);

    openDropdown = signal<string | null>(null);

    isActiveRoute(route: string): boolean {
        return this.router.url.startsWith(route);
    }

    toggleDropdown(dropdown: string): void {
        if (this.openDropdown() === dropdown) {
            this.openDropdown.set(null);
        } else {
            this.openDropdown.set(dropdown);
        }
    }

    closeDropdown(): void {
        this.openDropdown.set(null);
    }

    isDropdownOpen(dropdown: string): boolean {
        return this.openDropdown() === dropdown;
    }
}
