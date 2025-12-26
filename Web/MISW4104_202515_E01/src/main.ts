/// <reference types="@angular/localize" />

import { BrowserModule, bootstrapApplication } from '@angular/platform-browser';
import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';
import { importProvidersFrom } from '@angular/core';
import {
    provideHttpClient,
    withFetch,
    withInterceptors,
} from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideToastr } from 'ngx-toastr';
import { httpErrorInterceptor } from './app/shared/interceptors/http-error.interceptor';

bootstrapApplication(AppComponent, {
    providers: [
        provideHttpClient(
            withFetch(),
            withInterceptors([httpErrorInterceptor]),
        ),
        importProvidersFrom(BrowserModule),
        provideRouter(routes),
        provideAnimations(),
        provideToastr(),
    ],
}).catch((err) => console.error(err));
