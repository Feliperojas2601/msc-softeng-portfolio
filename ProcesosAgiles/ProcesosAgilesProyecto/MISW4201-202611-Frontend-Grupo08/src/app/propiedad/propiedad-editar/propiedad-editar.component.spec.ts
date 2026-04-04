import { of, throwError } from 'rxjs';
import { Propiedad } from '../propiedad';
import { ToastrModule } from 'ngx-toastr';
import { ReactiveFormsModule } from '@angular/forms';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { PropiedadService } from '../propiedad.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PropiedadEditarComponent } from './propiedad-editar.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('PropiedadEditarComponent', () => {
    let component: PropiedadEditarComponent;
    let fixture: ComponentFixture<PropiedadEditarComponent>;
    let propiedadServiceSpy: jasmine.SpyObj<PropiedadService>;
    let enumsServiceSpy: jasmine.SpyObj<EnumsService>;
    let errorServiceSpy: jasmine.SpyObj<ErrorService>;
    let activeModalSpy: jasmine.SpyObj<NgbActiveModal>;

    const mockPropietarios = [
        { id: 1, usuario: 'propietario_1' },
        { id: 2, usuario: 'propietario_2' },
    ];

    const mockBancos = ['BANCOLOMBIA', 'DAVIVIENDA'];

    const mockPropiedad = new Propiedad(
        1, 'Casa Campestre', 'Bogotá', 'Usaquén', 'Calle 100',
        'propietario_1', '3001234567', 'BANCOLOMBIA', '123456'
    );

    beforeEach(async () => {
        propiedadServiceSpy = jasmine.createSpyObj('PropiedadService', [
            'darPropiedades', 'darPropiedad', 'crearPropiedad', 'editarPropiedad',
            'borrarPropiedad', 'darPropietarios'
        ]);
        propiedadServiceSpy.darPropietarios.and.returnValue(of(mockPropietarios));
        propiedadServiceSpy.darPropiedad.and.returnValue(of(mockPropiedad));
        propiedadServiceSpy.editarPropiedad.and.returnValue(of(mockPropiedad));

        enumsServiceSpy = jasmine.createSpyObj('EnumsService', ['bancos']);
        enumsServiceSpy.bancos.and.returnValue(of(mockBancos));
        errorServiceSpy = jasmine.createSpyObj('ErrorService', ['manejarError']);
        activeModalSpy = jasmine.createSpyObj('NgbActiveModal', ['close', 'dismiss']);

        await TestBed.configureTestingModule({
            imports: [
                PropiedadEditarComponent,
                ToastrModule.forRoot(),
                NoopAnimationsModule,
                ReactiveFormsModule
            ],
            providers: [
                { provide: PropiedadService, useValue: propiedadServiceSpy },
                { provide: EnumsService, useValue: enumsServiceSpy },
                { provide: ErrorService, useValue: errorServiceSpy },
                { provide: NgbActiveModal, useValue: activeModalSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(PropiedadEditarComponent);
        component = fixture.componentInstance;
        component.idPropiedad = 1;
        fixture.detectChanges();
    });

    it('should create the component', () => {
        expect(component).toBeTruthy();
    });

    it('should call darPropietarios on ngOnInit', () => {
        expect(propiedadServiceSpy.darPropietarios).toHaveBeenCalled();
    });

    it('should populate listaPropietarios from service response', () => {
        expect(component.listaPropietarios.length).toBe(2);
        expect(component.listaPropietarios[0].usuario).toBe('propietario_1');
        expect(component.listaPropietarios[1].usuario).toBe('propietario_2');
    });

    it('should call darPropiedad on ngOnInit', () => {
        expect(propiedadServiceSpy.darPropiedad).toHaveBeenCalledWith(1);
    });

    it('should pre-fill the form with existing propiedad data', () => {
        expect(component.propiedadForm.get('nombre_propiedad')!.value).toBe('Casa Campestre');
        expect(component.propiedadForm.get('ciudad')!.value).toBe('Bogotá');
        expect(component.propiedadForm.get('nombre_propietario')!.value).toBe('propietario_1');
    });

    it('should have form invalid when nombre_propietario is empty', () => {
        component.propiedadForm.get('nombre_propietario')!.setValue('');
        expect(component.propiedadForm.get('nombre_propietario')!.invalid).toBeTrue();
    });

    it('should pre-select the matching option in the select element', () => {
        fixture.detectChanges();
        const compiled = fixture.nativeElement as HTMLElement;
        const selects = compiled.querySelectorAll('select');
        const propietarioSelect = Array.from(selects).find(s =>
            s.innerHTML.includes('propietario_1')
        ) as HTMLSelectElement;
        const selectedOption = propietarioSelect?.options[propietarioSelect.selectedIndex];
        expect(selectedOption?.textContent?.trim()).toBe('propietario_1');
    });

    it('should load propietarios and propiedad together before building form', () => {
        expect(propiedadServiceSpy.darPropietarios).toHaveBeenCalled();
        expect(propiedadServiceSpy.darPropiedad).toHaveBeenCalledWith(1);
        expect(component.listaPropietarios.length).toBe(2);
        expect(component.propiedadForm.get('nombre_propietario')!.value).toBe('propietario_1');
    });

    it('should call activeModal.dismiss on cancelar', () => {
        component.cancelar();
        expect(activeModalSpy.dismiss).toHaveBeenCalled();
    });

    it('should call activeModal.close with true on successful editar', () => {
        component.editar();
        expect(activeModalSpy.close).toHaveBeenCalledWith(true);
    });

    it('should delegate editarPropiedad error to ErrorService', () => {
        const error = { status: 401 };
        propiedadServiceSpy.editarPropiedad.and.returnValue(throwError(() => error));
        component.editar();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith(error);
    });

    it('should not call errorService on successful editar', () => {
        component.editar();
        expect(errorServiceSpy.manejarError).not.toHaveBeenCalled();
    });
});