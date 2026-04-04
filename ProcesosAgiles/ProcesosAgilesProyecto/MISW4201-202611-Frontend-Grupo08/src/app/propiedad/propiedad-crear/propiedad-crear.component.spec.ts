import { of, throwError } from 'rxjs';
import { ToastrModule } from 'ngx-toastr';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { ReactiveFormsModule } from '@angular/forms';
import { PropiedadService } from '../propiedad.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PropiedadCrearComponent } from './propiedad-crear.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('PropiedadCrearComponent', () => {
    let component: PropiedadCrearComponent;
    let fixture: ComponentFixture<PropiedadCrearComponent>;
    let propiedadServiceSpy: jasmine.SpyObj<PropiedadService>;
    let enumsServiceSpy: jasmine.SpyObj<EnumsService>;
    let errorServiceSpy: jasmine.SpyObj<ErrorService>;
    let activeModalSpy: jasmine.SpyObj<NgbActiveModal>;

    const mockPropietarios = [
        { id: 1, usuario: 'propietario_1' },
        { id: 2, usuario: 'propietario_2' },
    ];

    const mockBancos = ['BANCOLOMBIA', 'DAVIVIENDA'];

    beforeEach(async () => {
        propiedadServiceSpy = jasmine.createSpyObj('PropiedadService', [
            'darPropiedades', 'darPropiedad', 'crearPropiedad', 'editarPropiedad',
            'borrarPropiedad', 'darPropietarios'
        ]);
        propiedadServiceSpy.darPropietarios.and.returnValue(of(mockPropietarios));
        propiedadServiceSpy.crearPropiedad.and.returnValue(of({} as any));

        enumsServiceSpy = jasmine.createSpyObj('EnumsService', ['bancos']);
        enumsServiceSpy.bancos.and.returnValue(of(mockBancos));

        errorServiceSpy = jasmine.createSpyObj('ErrorService', ['manejarError']);

        // ↓ Mockeamos NgbActiveModal con los métodos que usa el componente
        activeModalSpy = jasmine.createSpyObj('NgbActiveModal', ['close', 'dismiss']);

        await TestBed.configureTestingModule({
            imports: [
                PropiedadCrearComponent,
                ToastrModule.forRoot(),
                NoopAnimationsModule,
                ReactiveFormsModule
            ],
            providers: [
                { provide: PropiedadService, useValue: propiedadServiceSpy },
                { provide: EnumsService,     useValue: enumsServiceSpy },
                { provide: ErrorService,     useValue: errorServiceSpy },
                // ↓ Proveemos el mock de NgbActiveModal
                { provide: NgbActiveModal,   useValue: activeModalSpy }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(PropiedadCrearComponent);
        component = fixture.componentInstance;
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

    it('should render a select element for nombre_propietario', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const select = compiled.querySelector('select');
        expect(select).toBeTruthy();
    });

    it('should render options for each propietario', () => {
        fixture.detectChanges();
        const compiled = fixture.nativeElement as HTMLElement;
        // Buscamos el select que contiene las opciones de propietarios
        const selects = compiled.querySelectorAll('select');
        const propietarioSelect = Array.from(selects).find(s =>
            s.innerHTML.includes('propietario_1')
        );
        const options = propietarioSelect?.querySelectorAll('option');
        // +1 por la opción placeholder
        expect(options?.length).toBe(mockPropietarios.length + 1);
    });

    it('should have form invalid when nombre_propietario is empty', () => {
        component.propiedadForm.get('nombre_propietario')!.setValue('');
        expect(component.propiedadForm.get('nombre_propietario')!.invalid).toBeTrue();
    });

    it('should have form valid when all fields are filled', () => {
        component.propiedadForm.patchValue({
            nombre_propiedad:  'Casa',
            ciudad:            'Bogotá',
            municipio:         'Usaquén',
            direccion:         'Calle 100',
            nombre_propietario:'propietario_1',
            numero_contacto:   '3001234567',
            banco:             'BANCOLOMBIA',
            numero_cuenta:     '123456'
        });
        expect(component.propiedadForm.valid).toBeTrue();
    });

    it('should call activeModal.dismiss on cancelar', () => {
        component.cancelar();
        expect(activeModalSpy.dismiss).toHaveBeenCalled();
    });

    it('should call activeModal.close with true on successful guardar', () => {
        component.propiedadForm.patchValue({
            nombre_propiedad:  'Casa',
            ciudad:            'Bogotá',
            municipio:         'Usaquén',
            direccion:         'Calle 100',
            nombre_propietario:'propietario_1',
            numero_contacto:   '3001234567',
            banco:             'BANCOLOMBIA',
            numero_cuenta:     '123456'
        });
        component.guardar();
        expect(activeModalSpy.close).toHaveBeenCalledWith(true);
    });

    it('should delegate crearPropiedad error to ErrorService', () => {
        const error = { status: 401 };
        propiedadServiceSpy.crearPropiedad.and.returnValue(throwError(() => error));
        component.propiedadForm.patchValue({
            nombre_propiedad:  'Casa',
            ciudad:            'Bogotá',
            municipio:         'Usaquén',
            direccion:         'Calle 100',
            nombre_propietario:'propietario_1',
            numero_contacto:   '3001234567',
            banco:             'BANCOLOMBIA',
            numero_cuenta:     '123456'
        });
        component.guardar();
        expect(errorServiceSpy.manejarError).toHaveBeenCalledWith(error);
    });

    it('should not call errorService on successful crearPropiedad', () => {
        component.propiedadForm.patchValue({
            nombre_propiedad:  'Casa',
            ciudad:            'Bogotá',
            municipio:         'Usaquén',
            direccion:         'Calle 100',
            nombre_propietario:'propietario_1',
            numero_contacto:   '3001234567',
            banco:             'BANCOLOMBIA',
            numero_cuenta:     '123456'
        });
        component.guardar();
        expect(errorServiceSpy.manejarError).not.toHaveBeenCalled();
    });
});