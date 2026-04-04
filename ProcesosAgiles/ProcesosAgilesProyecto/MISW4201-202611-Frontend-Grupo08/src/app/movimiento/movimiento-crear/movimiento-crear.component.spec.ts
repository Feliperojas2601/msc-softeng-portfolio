import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ToastrModule } from 'ngx-toastr';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of, throwError } from 'rxjs';
import { ReactiveFormsModule } from '@angular/forms';
import { provideHttpClient } from '@angular/common/http';

import { MovimientoCrearComponent } from './movimiento-crear.component';
import { MovimientoService } from '../movimiento.service';
import { ReservaService } from 'src/app/reserva/reserva.service';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { CategoriaService } from 'src/app/categoria/categoria.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

describe('MovimientoCrearComponent', () => {
    let component: MovimientoCrearComponent;
    let fixture: ComponentFixture<MovimientoCrearComponent>;
    let movimientoServiceSpy: jasmine.SpyObj<MovimientoService>;
    let reservaServiceSpy: jasmine.SpyObj<ReservaService>;
    let enumsServiceSpy: jasmine.SpyObj<EnumsService>;
    let errorServiceSpy: jasmine.SpyObj<ErrorService>;
    let categoriaServiceSpy: jasmine.SpyObj<CategoriaService>;
    let activeModalSpy: jasmine.SpyObj<NgbActiveModal>;

    const mockReservas        = [{ id: 1, nombre: 'Huésped A' }, { id: 2, nombre: 'Huésped B' }];
    const mockTiposMovimiento = ['INGRESO', 'EGRESO'];
    const mockCategorias      = [{ id: 1, nombre: 'Limpieza' }, { id: 2, nombre: 'Mantenimiento' }];

    beforeEach(async () => {
        movimientoServiceSpy = jasmine.createSpyObj('MovimientoService', ['crearMovimiento']);
        reservaServiceSpy    = jasmine.createSpyObj('ReservaService', ['obtenerReservas']);
        enumsServiceSpy      = jasmine.createSpyObj('EnumsService', ['tiposMovimiento']);
        errorServiceSpy      = jasmine.createSpyObj('ErrorService', ['manejarError']);
        categoriaServiceSpy  = jasmine.createSpyObj('CategoriaService', ['darCategorias']);
        activeModalSpy       = jasmine.createSpyObj('NgbActiveModal', ['close', 'dismiss']);

        reservaServiceSpy.obtenerReservas.and.returnValue(of(mockReservas as any));
        enumsServiceSpy.tiposMovimiento.and.returnValue(of(mockTiposMovimiento as any));
        categoriaServiceSpy.darCategorias.and.returnValue(of(mockCategorias as any));
        movimientoServiceSpy.crearMovimiento.and.returnValue(of({} as any));

        await TestBed.configureTestingModule({
            imports: [
                MovimientoCrearComponent,
                ToastrModule.forRoot(),
                NoopAnimationsModule,
                ReactiveFormsModule
            ],
            providers: [
                provideHttpClient(),   // ← necesario por CategoriaSelectorComponent
                { provide: MovimientoService, useValue: movimientoServiceSpy },
                { provide: ReservaService,    useValue: reservaServiceSpy },
                { provide: EnumsService,      useValue: enumsServiceSpy },
                { provide: ErrorService,      useValue: errorServiceSpy },
                { provide: CategoriaService,  useValue: categoriaServiceSpy },
                { provide: NgbActiveModal,    useValue: activeModalSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(MovimientoCrearComponent);
        component = fixture.componentInstance;
        component.idPropiedad = 5;
        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should call obtenerReservas with idPropiedad on init', () => {
        expect(reservaServiceSpy.obtenerReservas).toHaveBeenCalledWith(5);
    });

    it('should call tiposMovimiento on init', () => {
        expect(enumsServiceSpy.tiposMovimiento).toHaveBeenCalled();
    });

    it('should call darCategorias on init', () => {
        expect(categoriaServiceSpy.darCategorias).toHaveBeenCalled();
    });

    it('should call the 3 services at least once on init', () => {
        // darCategorias se llama 2 veces: una en MovimientoCrearComponent y otra en CategoriaSelectorComponent
        expect(reservaServiceSpy.obtenerReservas).toHaveBeenCalledTimes(1);
        expect(enumsServiceSpy.tiposMovimiento).toHaveBeenCalledTimes(1);
        expect(categoriaServiceSpy.darCategorias).toHaveBeenCalled();
    });

    it('should populate listaReservas after init', () => {
        expect(component.listaReservas).toEqual(mockReservas as any);
    });

    it('should populate tiposMovimiento after init', () => {
        expect(component.tiposMovimiento).toEqual(mockTiposMovimiento as any);
    });

    it('should populate listaCategorias after init', () => {
        expect(component.listaCategorias).toEqual(mockCategorias as any);
    });

    it('should initialize movimientoForm with required fields', () => {
        expect(component.movimientoForm).toBeTruthy();
        expect(component.movimientoForm.get('fecha')).toBeTruthy();
        expect(component.movimientoForm.get('concepto')).toBeTruthy();
        expect(component.movimientoForm.get('valor')).toBeTruthy();
        expect(component.movimientoForm.get('tipo_movimiento')).toBeTruthy();
        expect(component.movimientoForm.get('id_categoria')).toBeTruthy();
    });

    it('should have form invalid when required fields are empty', () => {
        expect(component.movimientoForm.invalid).toBeTrue();
    });

    it('should not call errorService on successful init', () => {
        expect(errorServiceSpy.manejarError).not.toHaveBeenCalled();
    });

    it('should delegate init error to ErrorService', () => {
        reservaServiceSpy.obtenerReservas.and.returnValue(throwError(() => ({ status: 401 })));
        component.ngOnInit();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith({ status: 401 });
    });

    it('should call activeModal.close with true on successful guardar', () => {
        component.movimientoForm.patchValue({
            fecha: '2026-03-01T10:00',
            concepto: 'Test',
            valor: 100000,
            tipo_movimiento: 'INGRESO',
            id_categoria: 1,
            id_reserva: null
        });
        component.guardar();
        expect(activeModalSpy.close).toHaveBeenCalledWith(true);
    });

    it('should delegate guardar error to ErrorService', () => {
        movimientoServiceSpy.crearMovimiento.and.returnValue(throwError(() => ({ status: 500 })));
        component.movimientoForm.patchValue({
            fecha: '2026-03-01T10:00',
            concepto: 'Test',
            valor: 100000,
            tipo_movimiento: 'INGRESO',
            id_categoria: 1,
            id_reserva: null
        });
        component.guardar();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith({ status: 500 });
    });

    it('should call activeModal.close on cancelar', () => {
        // cancelar() llama close(true), no dismiss()
        component.cancelar();
        expect(activeModalSpy.close).toHaveBeenCalledWith(true);
    });

    it('should not submit form when invalid', () => {
        component.guardar();
        expect(movimientoServiceSpy.crearMovimiento).not.toHaveBeenCalled();
    });
});