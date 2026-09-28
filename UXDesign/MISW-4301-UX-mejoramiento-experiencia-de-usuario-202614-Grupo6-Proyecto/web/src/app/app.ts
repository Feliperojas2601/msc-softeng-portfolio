// Libraries
import { RouterOutlet } from '@angular/router';
import { Component, signal } from '@angular/core';

// Application component
@Component({
  imports: [RouterOutlet],
  selector: 'app-root',
  styleUrl: './app.scss',
  templateUrl: './app.html',
})
export class App { protected readonly title = signal('snoozeless-web'); }
