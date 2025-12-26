import { ComponentFixture, TestBed } from '@angular/core/testing';
import { InputFieldComponent } from './input-field.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

describe('InputFieldComponent', () => {
    let component: InputFieldComponent;
    let fixture: ComponentFixture<InputFieldComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [InputFieldComponent, FormsModule, ReactiveFormsModule],
        }).compileComponents();

        fixture = TestBed.createComponent(InputFieldComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should render input element when type is not textarea', () => {
        component.type = 'text';
        component.label = 'Test Label';
        fixture.detectChanges();

        const compiled = fixture.nativeElement;
        const input = compiled.querySelector('input');
        expect(input).toBeTruthy();
    });

    it('should render textarea element when type is textarea', () => {
        component.type = 'textarea';
        component.label = 'Test Label';
        fixture.detectChanges();

        const compiled = fixture.nativeElement;
        const textarea = compiled.querySelector('textarea');
        expect(textarea).toBeTruthy();
    });

    it('should display error message when error is provided', () => {
        component.error = 'Este campo es requerido';
        fixture.detectChanges();

        const compiled = fixture.nativeElement;
        const errorDiv = compiled.querySelector('.invalid-feedback');
        expect(errorDiv).toBeTruthy();
        expect(errorDiv.textContent).toContain('Este campo es requerido');
    });

    it('should not display error message when error is null', () => {
        component.error = null;
        fixture.detectChanges();

        const compiled = fixture.nativeElement;
        const errorDiv = compiled.querySelector('.invalid-feedback');
        expect(errorDiv).toBeFalsy();
    });

    it('should call onChange when input value changes', () => {
        spyOn(component, 'onChange');
        component.type = 'text';
        fixture.detectChanges();

        const input = fixture.nativeElement.querySelector('input');
        input.value = 'test value';
        input.dispatchEvent(new Event('input'));

        expect(component.onChange).toHaveBeenCalledWith('test value');
    });

    it('should call onTouched when input is blurred', () => {
        spyOn(component, 'onTouched');
        component.type = 'text';
        fixture.detectChanges();

        const input = fixture.nativeElement.querySelector('input');
        input.dispatchEvent(new Event('blur'));

        expect(component.onTouched).toHaveBeenCalled();
    });

    it('should disable input when setDisabledState is called with true', () => {
        component.type = 'text';
        fixture.detectChanges();

        component.setDisabledState(true);
        fixture.detectChanges();

        const input = fixture.nativeElement.querySelector('input');
        expect(input.disabled).toBeTruthy();
    });

    it('should write value when writeValue is called', () => {
        component.writeValue('test value');
        expect(component.value).toBe('test value');
    });

    it('should handle empty value in writeValue', () => {
        component.writeValue(null);
        expect(component.value).toBe('');
    });
});
