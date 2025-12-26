import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LayoutComponent } from './shared/layout/layout.component';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss',
    imports: [RouterOutlet, LayoutComponent],
})
export class AppComponent {
    title = 'front';
    show = signal<string>('actors');

    set(view: string) {
        this.show.set(view);
    }
}
