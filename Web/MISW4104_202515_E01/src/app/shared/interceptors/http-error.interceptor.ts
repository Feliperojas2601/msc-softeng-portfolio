import {
    HttpEvent,
    HttpRequest,
    HttpErrorResponse,
    HttpInterceptorFn,
    HttpHandlerFn,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';
import { inject } from '@angular/core';

export const httpErrorInterceptor: HttpInterceptorFn = (
    req: HttpRequest<unknown>,
    next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> => {
    const toastr = inject(ToastrService);

    return next(req).pipe(
        catchError((httpErrorResponse: HttpErrorResponse) => {
            let errorMessage = '';
            let errorType = '';

            if (httpErrorResponse.error instanceof HttpErrorResponse) {
                errorType = 'Client side error';
                errorMessage = httpErrorResponse.statusText;
                toastr.error(errorMessage, errorType, {
                    closeButton: true,
                });
            } else {
                errorType = 'Server side error';
                if (httpErrorResponse.status === 0) {
                    errorMessage = 'No hay conexión con el servidor';
                } else {
                    errorMessage = `${httpErrorResponse.status}: ${httpErrorResponse.statusText}`;
                }

                toastr.error(errorMessage, errorType, {
                    closeButton: true,
                });
            }
            return throwError(() => new Error(errorMessage));
        }),
    );
};
