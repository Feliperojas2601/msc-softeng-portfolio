import { of, throwError } from 'rxjs';
import { Propiedad } from '../propiedad';
import { ErrorService } from 'src/app/error.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { PropiedadService } from '../propiedad.service';
import { Router, provideRouter } from '@angular/router';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PropiedadListaComponent } from './propiedad-lista.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('PropiedadListaComponent', () => {
    let component: PropiedadListaComponent;
    let fixture: ComponentFixture<PropiedadListaComponent>;
    let propiedadServiceSpy: jasmine.SpyObj<PropiedadService>;
    let errorServiceSpy: jasmine.SpyObj<ErrorService>;
    let modalServiceSpy: jasmine.SpyObj<NgbModal>;
    let router: Router;
    let toastr: ToastrService;

    const mockPropiedades: Propiedad[] = [
        new Propiedad(1, 'San Simon',   'Bogotá',   'Usaquén', 'Calle 100',  'Juan Pérez', '3001234567', 'Bancolombia', '123456'),
        new Propiedad(2, 'El Refugio',  'Medellín', 'Envigado','Carrera 43', 'Ana López',  '3009876543', 'Davivienda',  '654321'),
    ];

    beforeEach(async () => {
        propiedadServiceSpy = jasmine.createSpyObj('PropiedadService', ['darPropiedades', 'borrarPropiedad']);
        propiedadServiceSpy.darPropiedades.and.returnValue(of(mockPropiedades));

        errorServiceSpy = jasmine.createSpyObj('ErrorService', ['manejarError']);

        // ↓ Mockeamos NgbModal para que abrirModalCrear y editarPropiedad no fallen
        modalServiceSpy = jasmine.createSpyObj('NgbModal', ['open']);
        modalServiceSpy.open.and.returnValue({
            componentInstance: {},
            result: Promise.resolve(null)
        } as any);

        await TestBed.configureTestingModule({
            imports: [
                PropiedadListaComponent,
                ToastrModule.forRoot(),
                NoopAnimationsModule
            ],
            providers: [
                provideRouter([]),
                provideHttpClient(),
                { provide: PropiedadService, useValue: propiedadServiceSpy },
                { provide: ErrorService, useValue: errorServiceSpy },
                { provide: NgbModal, useValue: modalServiceSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(PropiedadListaComponent);
        component = fixture.componentInstance;
        router = TestBed.inject(Router);
        toastr = TestBed.inject(ToastrService);
        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should load propiedades on init', () => {
        expect(propiedadServiceSpy.darPropiedades).toHaveBeenCalled();
        expect(component.propiedades.length).toBe(2);
        expect(component.propiedades[0].nombre_propiedad).toBe('San Simon');
    });

    it('should render the title "Propiedades"', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const title = compiled.querySelector('.page-title');
        expect(title?.textContent).toContain('Propiedades');
    });

    it('should render the subtitle with property count', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const subtitle = compiled.querySelector('.page-subtitle');
        expect(subtitle?.textContent).toContain('2 propiedades registradas');
    });

    it('should NOT render columns for Dirección, Nombre propietario, or Contacto', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        expect(compiled.innerHTML).not.toContain('Dirección');
        expect(compiled.innerHTML).not.toContain('Nombre propietario');
        expect(compiled.innerHTML).not.toContain('Contacto');
    });

    it('should render a card for each propiedad', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const cards = compiled.querySelectorAll('.property-card');
        expect(cards.length).toBe(2);
    });

    it('should render 6 action buttons per card', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const firstCard = compiled.querySelector('.property-card');
        const buttons = firstCard?.querySelectorAll('.btn-action');
        expect(buttons?.length).toBe(6);
    });

    it('should render edit button with correct style and icon', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const editBtn = compiled.querySelector('.btn-edit');
        expect(editBtn).toBeTruthy();
        expect(editBtn?.querySelector('.bi-pencil-fill')).toBeTruthy();
    });

    it('should render delete button with correct style and icon', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const deleteBtn = compiled.querySelector('.btn-delete');
        expect(deleteBtn).toBeTruthy();
        expect(deleteBtn?.querySelector('.bi-trash-fill')).toBeTruthy();
    });

    it('should render movimientos button with correct style and icon', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const movimientosBtn = compiled.querySelector('.btn-movimientos');
        expect(movimientosBtn).toBeTruthy();
        expect(movimientosBtn?.querySelector('.bi-cash-coin')).toBeTruthy();
    });

    it('should render the add button with "+" icon and label', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const addBtn = compiled.querySelector('.btn-add');
        expect(addBtn).toBeTruthy();
        expect(addBtn?.querySelector('.bi-plus-lg')).toBeTruthy();
        expect(addBtn?.textContent).toContain('Nueva propiedad');
    });

    it('should call modalService.open on abrirModalCrear', () => {
        component.abrirModalCrear();
        expect(modalServiceSpy.open).toHaveBeenCalled();
    });

    it('should call modalService.open on editarPropiedad', () => {
        component.editarPropiedad(1);
        expect(modalServiceSpy.open).toHaveBeenCalled();
    });

    it('should navigate to reservas on reservas call', () => {
        spyOn(router, 'navigate');
        component.reservas(1);
        expect(router.navigate).toHaveBeenCalledWith(['/propiedades/1/reservas']);
    });

    it('should navigate to movimientos on movimientos call', () => {
        spyOn(router, 'navigate');
        component.movimientos(1);
        expect(router.navigate).toHaveBeenCalledWith(['/propiedades/1/movimientos']);
    });

    it('should delegate error to ErrorService on status 401', () => {
        const error = { status: 401 };
        propiedadServiceSpy.darPropiedades.and.returnValue(throwError(() => error));
        component.ngOnInit();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith(error);
    });

    it('should delegate error to ErrorService on status 422', () => {
        const error = { status: 422 };
        propiedadServiceSpy.darPropiedades.and.returnValue(throwError(() => error));
        component.ngOnInit();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith(error);
    });

    it('should delegate error to ErrorService on generic server error', () => {
        const error = { status: 500, message: 'Network error' };
        propiedadServiceSpy.darPropiedades.and.returnValue(throwError(() => error));
        component.ngOnInit();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith(error);
    });

    it('should call abrirModalCrear when add button is clicked', () => {
        spyOn(component, 'abrirModalCrear');
        const compiled = fixture.nativeElement as HTMLElement;
        const addBtn = compiled.querySelector('.btn-add') as HTMLButtonElement;
        addBtn.click();
        expect(component.abrirModalCrear).toHaveBeenCalled();
    });

    it('should call editarPropiedad when edit button is clicked', () => {
        spyOn(component, 'editarPropiedad');
        const compiled = fixture.nativeElement as HTMLElement;
        const editBtn = compiled.querySelector('.btn-edit') as HTMLButtonElement;
        editBtn.click();
        expect(component.editarPropiedad).toHaveBeenCalledWith(1);
    });

    it('should call movimientos when movimientos button is clicked', () => {
        spyOn(component, 'movimientos');
        const compiled = fixture.nativeElement as HTMLElement;
        const movimientosBtn = compiled.querySelector('.btn-movimientos') as HTMLButtonElement;
        movimientosBtn.click();
        expect(component.movimientos).toHaveBeenCalledWith(1);
    });

    it('should have no href attributes on action buttons (SPA)', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const actionBtns = compiled.querySelectorAll('.btn-action');
        actionBtns.forEach(btn => {
            expect(btn.getAttribute('href')).toBeNull();
        });
    });

    it('should render action button labels', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const labels = compiled.querySelectorAll('.btn-label');
        const labelTexts = Array.from(labels).map(l => l.textContent?.trim());
        expect(labelTexts).toContain('Editar');
        expect(labelTexts).toContain('Eliminar');
        expect(labelTexts).toContain('Movimientos');
    });

    it('should render card accent bars', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const accents = compiled.querySelectorAll('.card-accent');
        expect(accents.length).toBe(2);
    });

    it('should render card icons', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const icons = compiled.querySelectorAll('.card-icon .bi-buildings');
        expect(icons.length).toBe(2);
    });
});