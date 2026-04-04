import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of, throwError } from 'rxjs';
import { NgbActiveModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { ActividadMantenimientoEditarComponent } from './actividad-mantenimiento-editar.component';
import { ActividadMantenimientoService } from '../../actividad-mantenimiento.service';
import { ActividadMantenimiento } from '../../actividad-mantenimiento';
import { EnumsService } from 'src/app/enums.service';
import { PeriodicidadMantenimiento } from 'src/app/enums';

describe('ActividadMantenimientoEditarComponent', () => {
    let component: ActividadMantenimientoEditarComponent;
    let fixture: ComponentFixture<ActividadMantenimientoEditarComponent>;
    let actividadServiceSpy: jasmine.SpyObj<ActividadMantenimientoService>;
    let enumServiceSpy: jasmine.SpyObj<EnumsService>;
    let activeModalSpy: jasmine.SpyObj<NgbActiveModal>;
    let toastr: ToastrService;

    const mockActividad: ActividadMantenimiento = {
        id: 1,
        concepto: 'Limpieza filtros',
        categoria: 'LIMPIEZA',
        periodicidad: 'MENSUAL',
        estado: 'PROGRAMADO',
        fecha_registro: '2024-03-01',
        costo: 80000,
        id_propiedad: 1
    };

    beforeEach(async () => {
        actividadServiceSpy = jasmine.createSpyObj('ActividadMantenimientoService', ['editarActividadMantenimiento']);
        enumServiceSpy = jasmine.createSpyObj('EnumsService', ['tipoCategoriaMantenimiento', 'periodicidadMantenimiento']);
        activeModalSpy = jasmine.createSpyObj('NgbActiveModal', ['close', 'dismiss']);

        enumServiceSpy.tipoCategoriaMantenimiento.and.returnValue(of(['LIMPIEZA', 'REPARACION', 'REVISION'] as any));
        enumServiceSpy.periodicidadMantenimiento.and.returnValue(of([PeriodicidadMantenimiento.EVENTO, PeriodicidadMantenimiento.MENSUAL, PeriodicidadMantenimiento.TRIMESTRAL]));

        await TestBed.configureTestingModule({
            imports: [
                ActividadMantenimientoEditarComponent,
                NgbModule,
                ToastrModule.forRoot(),
                NoopAnimationsModule
            ],
            providers: [
                { provide: ActividadMantenimientoService, useValue: actividadServiceSpy },
                { provide: EnumsService, useValue: enumServiceSpy },
                { provide: NgbActiveModal, useValue: activeModalSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(ActividadMantenimientoEditarComponent);
        component = fixture.componentInstance;
        component.idPropiedad = 1;
        component.actividad = mockActividad;
        toastr = TestBed.inject(ToastrService);
        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should pre-populate the form with existing actividad values', () => {
        expect(component.editarForm.get('concepto')?.value).toBe(mockActividad.concepto);
        expect(component.editarForm.get('costo')?.value).toBe(mockActividad.costo);
    });

    it('should load categorias and periodicidades from enums service', () => {
        expect(enumServiceSpy.tipoCategoriaMantenimiento).toHaveBeenCalled();
        expect(enumServiceSpy.periodicidadMantenimiento).toHaveBeenCalled();
        expect(component.categorias.length).toBe(3);
        expect(component.periodicidades.length).toBe(3);
    });

    it('should disable guardar button when form is invalid', () => {
        component.editarForm.get('concepto')?.setValue('');
        fixture.detectChanges();
        const btn = fixture.nativeElement.querySelector('button.btn-primary') as HTMLButtonElement;
        expect(btn.disabled).toBeTrue();
    });

    it('should enable guardar button when form is valid', () => {
        fixture.detectChanges();
        const btn = fixture.nativeElement.querySelector('button.btn-primary') as HTMLButtonElement;
        expect(btn.disabled).toBeFalse();
    });

    it('should not call service when form is invalid and guardar() is called', () => {
        component.editarForm.get('concepto')?.setValue('');
        component.guardar();
        expect(actividadServiceSpy.editarActividadMantenimiento).not.toHaveBeenCalled();
    });

    it('should call editarActividadMantenimiento when guardar() is called with valid form', () => {
        actividadServiceSpy.editarActividadMantenimiento.and.returnValue(of(mockActividad));
        component.guardar();
        expect(actividadServiceSpy.editarActividadMantenimiento).toHaveBeenCalledWith(1, 1, component.editarForm.value);
    });

    it('should close activeModal with result on success', () => {
        const respuesta = { ...mockActividad, concepto: 'Limpieza profunda' };
        actividadServiceSpy.editarActividadMantenimiento.and.returnValue(of(respuesta));
        component.guardar();
        expect(activeModalSpy.close).toHaveBeenCalledWith(respuesta);
    });

    it('should set errorDuplicado on 409 error', () => {
        const errorMsg = 'Ya existe una actividad con ese concepto en esta propiedad';
        actividadServiceSpy.editarActividadMantenimiento.and.returnValue(
            throwError(() => ({ status: 409, error: { mensaje: errorMsg } }))
        );
        component.guardar();
        expect(component.errorDuplicado).toBe(errorMsg);
    });

    it('should show error toastr on non-409 error', () => {
        spyOn(toastr, 'error');
        actividadServiceSpy.editarActividadMantenimiento.and.returnValue(
            throwError(() => ({ status: 500 }))
        );
        component.guardar();
        expect(toastr.error).toHaveBeenCalledWith('Error al actualizar la actividad');
    });

    it('should dismiss activeModal when Cancelar is clicked', () => {
        const cancelBtn = fixture.nativeElement.querySelector('button.btn-secondary') as HTMLButtonElement;
        cancelBtn.click();
        expect(activeModalSpy.dismiss).toHaveBeenCalled();
    });

    it('should clear errorDuplicado before each save call', () => {
        component.errorDuplicado = 'previous error';
        actividadServiceSpy.editarActividadMantenimiento.and.returnValue(of(mockActividad));
        component.guardar();
        expect(component.errorDuplicado).toBe('');
    });
});
