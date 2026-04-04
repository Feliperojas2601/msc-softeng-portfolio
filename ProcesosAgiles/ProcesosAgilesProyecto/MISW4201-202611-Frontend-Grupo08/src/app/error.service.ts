import { Injectable } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Injectable({
    providedIn: 'root'
})
export class ErrorService {

    constructor(private toastr: ToastrService) { }

    manejarError(error: any): void {
        if (error.status === 401) {
            this.toastr.error('Error', 'Su sesión ha caducado, por favor vuelva a iniciar sesión.');
        } else if (error.status === 403) {
            const mensaje = error.error?.mensaje || 'No tiene permisos para realizar esta acción.';
            this.toastr.error('Acceso denegado', mensaje);
        } else if (error.status === 422) {
            this.toastr.error('Error', 'No hemos podido identificarlo, por favor vuelva a iniciar sesión.');
        } else {
            this.toastr.error('Error', 'Ha ocurrido un error. ' + error.message);
        }
    }
}
