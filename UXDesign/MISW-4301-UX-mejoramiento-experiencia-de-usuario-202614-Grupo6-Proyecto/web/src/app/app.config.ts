// Libraries
import { routes } from './app.routes';
import { provideRouter } from '@angular/router';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

// Application configuration
export const appConfig: ApplicationConfig = { providers: [ provideBrowserGlobalErrorListeners(), provideRouter(routes)] };
