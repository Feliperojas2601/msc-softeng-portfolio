import { TestBed } from '@angular/core/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

import { ErrorService } from './error.service';

describe('ErrorService', () => {
    let service: ErrorService;
    let toastr: ToastrService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [ToastrModule.forRoot(), NoopAnimationsModule],
            providers: [ErrorService]
        });
        service = TestBed.inject(ErrorService);
        toastr = TestBed.inject(ToastrService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should show session expired message on status 401', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 401, message: '' });
        expect(toastr.error).toHaveBeenCalledWith(
            'Error',
            'Su sesión ha caducado, por favor vuelva a iniciar sesión.'
        );
    });

    it('should show unprocessable entity message on status 422', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 422, message: '' });
        expect(toastr.error).toHaveBeenCalledWith(
            'Error',
            'No hemos podido identificarlo, por favor vuelva a iniciar sesión.'
        );
    });

    it('should show generic error with message on status 500', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 500, message: 'Internal Server Error' });
        expect(toastr.error).toHaveBeenCalledWith(
            'Error',
            'Ha ocurrido un error. Internal Server Error'
        );
    });

    it('should show generic error on network failure (status 0)', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 0, message: 'Unknown Error' });
        expect(toastr.error).toHaveBeenCalledWith(
            'Error',
            'Ha ocurrido un error. Unknown Error'
        );
    });

    it('should show backend message on status 403 with error body', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 403, error: { mensaje: 'Acceso denegado: Solo los propietarios pueden crear propiedades' } });
        expect(toastr.error).toHaveBeenCalledWith(
            'Acceso denegado',
            'Acceso denegado: Solo los propietarios pueden crear propiedades'
        );
    });

    it('should show default message on status 403 without error body', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 403, error: {} });
        expect(toastr.error).toHaveBeenCalledWith(
            'Acceso denegado',
            'No tiene permisos para realizar esta acción.'
        );
    });

    it('should call toastr.error exactly once per invocation', () => {
        spyOn(toastr, 'error');
        service.manejarError({ status: 401, message: '' });
        expect(toastr.error).toHaveBeenCalledTimes(1);
    });
});
