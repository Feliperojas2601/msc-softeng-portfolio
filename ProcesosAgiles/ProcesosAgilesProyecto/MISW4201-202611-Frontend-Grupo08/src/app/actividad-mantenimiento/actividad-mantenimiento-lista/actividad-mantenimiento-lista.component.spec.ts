import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of, throwError } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { ActividadMantenimientoListaComponent } from './actividad-mantenimiento-lista.component';
import { ActividadMantenimientoService } from '../actividad-mantenimiento.service';
import { ActividadMantenimiento } from '../actividad-mantenimiento';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';

describe('ElementoPropiedadListaComponent', () => {
    let component: ActividadMantenimientoListaComponent;
    let fixture: ComponentFixture<ActividadMantenimientoListaComponent>;
    let actividadServiceSpy: jasmine.SpyObj<ActividadMantenimientoService>;
    let toastrService: ToastrService;
    let modalService: NgbModal;
    let toastr: ToastrService;

    const mockElementos: ActividadMantenimiento[] = [
        { id: 1, concepto: 'lubricacion', categoria: 'LIMPIEZA', periodicidad: 'diario', estado: 'PROGRAMADO', fecha_registro: '2026-02-24', costo: 100, id_propiedad: 1 },
        { id: 2, concepto: 'lavado', categoria: 'LIMPIEZA', periodicidad: 'diario', estado: 'CANCELADO', fecha_registro: '2026-02-22', costo: 200, id_propiedad: 1 }
    ];

    beforeEach(async () => {
        actividadServiceSpy = jasmine.createSpyObj('ActividadMantenimientoService', ['darActividadesMantenimiento', 'eliminarActividadMantenimiento']);
        actividadServiceSpy.darActividadesMantenimiento.and.returnValue(of(mockElementos));

        await TestBed.configureTestingModule({
            imports: [
                ActividadMantenimientoListaComponent, 
                NgbModule,
                ToastrModule.forRoot(),
                NoopAnimationsModule
            ],
            providers: [
                provideRouter([]),
                provideHttpClient(),
                { provide: ActividadMantenimientoService, useValue: actividadServiceSpy },
                {
                    provide: ActivatedRoute,
                    useValue: {
                        snapshot: { paramMap: { get: () => '1' } } // Simula idPropiedad = 1
                    }
                }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(ActividadMantenimientoListaComponent);
        component = fixture.componentInstance;
        modalService = TestBed.inject(NgbModal);
        toastr = TestBed.inject(ToastrService);
        toastrService = TestBed.inject(ToastrService);
        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should load actividades on init', () => {
        expect(actividadServiceSpy.darActividadesMantenimiento).toHaveBeenCalledWith(1);
        expect(component.actividades.length).toBe(2);
    });

    it('should render the title and subtitle', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        expect(compiled.querySelector('.page-title')?.textContent).toContain('Actividades de Mantenimiento');
        expect(compiled.querySelector('.page-subtitle')?.textContent).toContain('2 actividades');
    });

    it('should render a table row for each actividad', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const rows = compiled.querySelectorAll('tbody tr');
        expect(rows.length).toBe(2);
    });

    it('should open ModalCrear when clicking Nuevo Actividad button', () => {
        spyOn(modalService, 'open').and.callThrough();
        const addBtn = fixture.nativeElement.querySelector('.btn-add') as HTMLButtonElement;
        addBtn.click();
        expect(modalService.open).toHaveBeenCalled();
    });

    it('should render the edit button in the detail panel when an actividad is selected', () => {
        component.seleccionarActividad(mockElementos[0]);
        fixture.detectChanges();
        const editBtn = fixture.nativeElement.querySelector('.btn-editar') as HTMLButtonElement;
        expect(editBtn).toBeTruthy();
    });

    it('should open modal when abrirModalEditar is called', () => {
        spyOn(modalService, 'open').and.returnValue({ componentInstance: {}, result: Promise.resolve(null) } as any);
        component.abrirModalEditar(mockElementos[0]);
        expect(modalService.open).toHaveBeenCalled();
    });

    it('should reload actividades after successful edit', async () => {
        const mockResult = { ...mockElementos[0], concepto: 'lubricacion actualizada' };
        spyOn(modalService, 'open').and.returnValue({
            componentInstance: {},
            result: Promise.resolve(mockResult)
        } as any);
        actividadServiceSpy.darActividadesMantenimiento.and.returnValue(of(mockElementos));
        component.abrirModalEditar(mockElementos[0]);
        await fixture.whenStable();
        expect(actividadServiceSpy.darActividadesMantenimiento).toHaveBeenCalledTimes(2);
    });

    it('should not reload actividades when edit modal is dismissed', async () => {
        spyOn(modalService, 'open').and.returnValue({
            componentInstance: {},
            result: Promise.reject('dismissed')
        } as any);
        actividadServiceSpy.darActividadesMantenimiento.calls.reset();
        component.abrirModalEditar(mockElementos[0]);
        await fixture.whenStable();
        expect(actividadServiceSpy.darActividadesMantenimiento).not.toHaveBeenCalled();
    });

});