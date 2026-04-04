import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ToastrModule } from 'ngx-toastr';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of, throwError } from 'rxjs';
import { ReactiveFormsModule } from '@angular/forms';
import { provideHttpClient } from '@angular/common/http';

import { MovimientoEditarComponent } from './movimiento-editar.component';
import { MovimientoService } from '../movimiento.service';
import { ReservaService } from 'src/app/reserva/reserva.service';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { CategoriaService } from 'src/app/categoria/categoria.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

describe('MovimientoEditarComponent', () => {
    let component: MovimientoEditarComponent;
    let fixture: ComponentFixture<MovimientoEditarComponent>;
    let movimientoServiceSpy: jasmine.SpyObj<MovimientoService>;
    let reservaServiceSpy: jasmine.SpyObj<ReservaService>;
    let enumsServiceSpy: jasmine.SpyObj<EnumsService>;
    let errorServiceSpy: jasmine.SpyObj<ErrorService>;
    let categoriaServiceSpy: jasmine.SpyObj<CategoriaService>;
    let activeModalSpy: jasmine.SpyObj<NgbActiveModal>;

    const mockMovimiento = {
        id: 1,
        fecha: new Date('2026-03-01'),
        concepto: 'Arriendo',
        valor: 500000,
        tipo_movimiento: 'INGRESO',
        id_categoria: 2,
        id_reserva: null,
        id_propiedad: 5
    };
    const mockReservas = [{ id: 1, nombre: 'Huésped A' }, { id: 2, nombre: 'Huésped B' }];
    const mockTiposMovimiento = ['INGRESO', 'EGRESO'];
    const mockCategorias = [{ id: 1, nombre: 'Limpieza' }, { id: 2, nombre: 'Mantenimiento' }];

    beforeEach(async () => {
        movimientoServiceSpy = jasmine.createSpyObj('MovimientoService', ['obtenerMovimiento', 'actualizarMovimiento']);
        reservaServiceSpy = jasmine.createSpyObj('ReservaService', ['obtenerReservas']);
        enumsServiceSpy = jasmine.createSpyObj('EnumsService', ['tiposMovimiento']);
        errorServiceSpy = jasmine.createSpyObj('ErrorService', ['manejarError']);
        categoriaServiceSpy = jasmine.createSpyObj('CategoriaService', ['darCategorias']);
        activeModalSpy = jasmine.createSpyObj('NgbActiveModal', ['close', 'dismiss']);

        movimientoServiceSpy.obtenerMovimiento.and.returnValue(of(mockMovimiento as any));
        movimientoServiceSpy.actualizarMovimiento.and.returnValue(of(mockMovimiento as any));
        reservaServiceSpy.obtenerReservas.and.returnValue(of(mockReservas as any));
        enumsServiceSpy.tiposMovimiento.and.returnValue(of(mockTiposMovimiento as any));
        categoriaServiceSpy.darCategorias.and.returnValue(of(mockCategorias as any));

        await TestBed.configureTestingModule({
            imports: [
                MovimientoEditarComponent,
                ToastrModule.forRoot(),
                NoopAnimationsModule,
                ReactiveFormsModule
            ],
            providers: [
                provideHttpClient(),
                { provide: MovimientoService, useValue: movimientoServiceSpy },
                { provide: ReservaService, useValue: reservaServiceSpy },
                { provide: EnumsService, useValue: enumsServiceSpy },
                { provide: ErrorService, useValue: errorServiceSpy },
                { provide: CategoriaService, useValue: categoriaServiceSpy },
                { provide: NgbActiveModal, useValue: activeModalSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(MovimientoEditarComponent);
        component = fixture.componentInstance;

        // @Input() asignados antes de ngOnInit
        component.idMovimiento = 1;
        component.idPropiedad = 5;

        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should call obtenerMovimiento with idMovimiento on init', () => {
        expect(movimientoServiceSpy.obtenerMovimiento).toHaveBeenCalledWith(1);
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

    it('should populate listaReservas after init', () => {
        expect(component.listaReservas).toEqual(mockReservas as any);
    });

    it('should populate tiposMovimiento after init', () => {
        expect(component.tiposMovimiento).toEqual(mockTiposMovimiento as any);
    });

    it('should populate listaCategorias after init', () => {
        expect(component.listaCategorias).toEqual(mockCategorias as any);
    });

    it('should patch form with movimiento data after init', () => {
        expect(component.movimientoForm.get('concepto')?.value).toBe('Arriendo');
        expect(component.movimientoForm.get('valor')?.value).toBe(500000);
        expect(component.movimientoForm.get('tipo_movimiento')?.value).toBe('INGRESO');
        expect(component.movimientoForm.get('id_categoria')?.value).toBe(2);
    });

    it('should initialize movimientoForm with required fields', () => {
        expect(component.movimientoForm).toBeTruthy();
        expect(component.movimientoForm.get('fecha')).toBeTruthy();
        expect(component.movimientoForm.get('concepto')).toBeTruthy();
        expect(component.movimientoForm.get('valor')).toBeTruthy();
        expect(component.movimientoForm.get('tipo_movimiento')).toBeTruthy();
        expect(component.movimientoForm.get('id_categoria')).toBeTruthy();
    });

    it('should not call errorService on successful init', () => {
        expect(errorServiceSpy.manejarError).not.toHaveBeenCalled();
    });

    it('should delegate init error to ErrorService', () => {
        movimientoServiceSpy.obtenerMovimiento.and.returnValue(throwError(() => ({ status: 401 })));
        reservaServiceSpy.obtenerReservas.and.returnValue(throwError(() => ({ status: 401 })));
        component.ngOnInit();
        expect(errorServiceSpy.manejarError).toHaveBeenCalled();
    });

    it('should call activeModal.close with true on successful editar', () => {
        component.editar();
        expect(activeModalSpy.close).toHaveBeenCalledWith(true);
    });

    it('should delegate editar error to ErrorService', () => {
        movimientoServiceSpy.actualizarMovimiento.and.returnValue(throwError(() => ({ status: 500 })));
        component.editar();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith({ status: 500 });
    });

    it('should not call actualizarMovimiento when form is invalid', () => {
        component.movimientoForm.patchValue({ concepto: '', valor: '', fecha: '', tipo_movimiento: '', id_categoria: '' });
        component.editar();
        expect(movimientoServiceSpy.actualizarMovimiento).not.toHaveBeenCalled();
    });

    it('should call activeModal.dismiss on cancelar', () => {
        component.cancelar();
        expect(activeModalSpy.dismiss).toHaveBeenCalled();
    });
});