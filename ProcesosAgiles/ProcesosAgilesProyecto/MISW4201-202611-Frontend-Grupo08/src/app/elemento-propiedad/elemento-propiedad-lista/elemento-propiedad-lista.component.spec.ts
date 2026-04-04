import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of, throwError } from 'rxjs';
import { ActivatedRoute } from '@angular/router';

import { ElementoPropiedadListaComponent } from './elemento-propiedad-lista.component';
import { ElementoPropiedadService } from '../elemento-propiedad.service';
import { ElementoPropiedad } from '../elemento-propiedad';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';

describe('ElementoPropiedadListaComponent', () => {
    let component: ElementoPropiedadListaComponent;
    let fixture: ComponentFixture<ElementoPropiedadListaComponent>;
    let elementoServiceSpy: jasmine.SpyObj<ElementoPropiedadService>;
    let modalService: NgbModal;
    let toastr: ToastrService;

    const mockElementos: ElementoPropiedad[] = [
        { id: 1, nombre: 'Nevera LG', tipo: 'Electrodoméstico', estado: 'Excelente', zona: 'Cocina', descripcion: 'Nevera no frost', fecha_registro: '2024-01-01', id_propiedad: 1 },
        { id: 2, nombre: 'Sofá 3 puestos', tipo: 'Mueble', estado: 'Dañado', zona: 'Sala', descripcion: 'Cuero sintético', fecha_registro: '2024-01-02', id_propiedad: 1 }
    ];

    beforeEach(async () => {
        elementoServiceSpy = jasmine.createSpyObj('ElementoPropiedadService', ['darElementosPropiedad', 'borrarElementoPropiedad']);        
        elementoServiceSpy.darElementosPropiedad.and.returnValue(of(mockElementos));

        await TestBed.configureTestingModule({
            imports: [
                ElementoPropiedadListaComponent, 
                NgbModule,
                ToastrModule.forRoot(),
                NoopAnimationsModule
            ],
            providers: [
                provideRouter([]),
                { provide: ElementoPropiedadService, useValue: elementoServiceSpy },
                {
                    provide: ActivatedRoute,
                    useValue: {
                        snapshot: { paramMap: { get: () => '1' } } // Simula idPropiedad = 1
                    }
                }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(ElementoPropiedadListaComponent);
        component = fixture.componentInstance;
        modalService = TestBed.inject(NgbModal);
        toastr = TestBed.inject(ToastrService);
        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should load elementos on init', () => {
        expect(elementoServiceSpy.darElementosPropiedad).toHaveBeenCalledWith(1);
        expect(component.elementos.length).toBe(2);
    });

    it('should render the title and subtitle', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        expect(compiled.querySelector('.page-title')?.textContent).toContain('Elementos de la Propiedad');
        expect(compiled.querySelector('.page-subtitle')?.textContent).toContain('2 elemento');
    });

    it('should render a table row for each elemento', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const rows = compiled.querySelectorAll('tbody tr');
        expect(rows.length).toBe(2);
    });

    it('should display the correct badge color for status', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const rows = compiled.querySelectorAll('tbody tr');
        expect(rows[0].querySelector('.estado-excelente')).toBeTruthy();
        expect(rows[1].querySelector('.estado-danado')).toBeTruthy();
    });

    it('should open ModalCrear when clicking Nuevo Elemento button', () => {
        spyOn(modalService, 'open').and.callThrough();
        const addBtn = fixture.nativeElement.querySelector('.btn-add') as HTMLButtonElement;
        addBtn.click();
        expect(modalService.open).toHaveBeenCalled();
    });

    it('should open ModalEditar when clicking edit button', () => {
        spyOn(modalService, 'open').and.callThrough();
        const row = fixture.nativeElement.querySelector('tbody tr') as HTMLElement;
        row.click();
        fixture.detectChanges();
        const editBtn = fixture.nativeElement.querySelector('.detail-actions .btn-edit') as HTMLButtonElement;
        editBtn.click();
        expect(modalService.open).toHaveBeenCalled();
    });

    it('should call delete flow when clicking delete button', () => {
        spyOn(component, 'eliminarElemento');
        const row = fixture.nativeElement.querySelector('tbody tr') as HTMLElement;
        row.click();
        fixture.detectChanges();
        const deleteBtn = fixture.nativeElement.querySelector('.detail-actions .btn-delete') as HTMLButtonElement;
        deleteBtn.click();
        expect(component.eliminarElemento).toHaveBeenCalledWith(mockElementos[0]);
    });

    it('should show error toastr if loading fails', () => {
        spyOn(toastr, 'error');
        elementoServiceSpy.darElementosPropiedad.and.returnValue(throwError(() => ({ statusText: 'Error' })));
        component.obtenerElementos();
        expect(toastr.error).toHaveBeenCalled();
    });
});