// Libraries
import { provideRouter } from '@angular/router';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalleAlarmaVivoComponent } from './detalle-alarma-vivo';

// Test
describe('DetalleAlarmaVivoComponent', () => {
    
    // Component
    let fixture: ComponentFixture<DetalleAlarmaVivoComponent>;

    // Before each test
    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [DetalleAlarmaVivoComponent],
            providers: [provideRouter([])],
        }).compileComponents();

        // Rendered HTML
        fixture = TestBed.createComponent(DetalleAlarmaVivoComponent);

        // Detect changes
        fixture.detectChanges();
    });

    // Test #1
    it('should create', () => {
        expect(fixture.componentInstance).toBeTruthy();
    });

    // Test #2
    it('should show the alarm name and time in the "sonando" banner', () => {
        
        // Rendered HTML
        const compiled = fixture.nativeElement as HTMLElement;

        // Assert #1
        expect(compiled.querySelector('.sonando__subtitle')?.textContent).toContain('Gym');

        // Assert #2
        expect(compiled.querySelector('.sonando__subtitle')?.textContent).toContain('06:30');
    });

    // Test #3
    it('should render the "Ir al reto" link pointing to the writing challenge', () => {
        
        // Rendered HTML        
        const compiled = fixture.nativeElement as HTMLElement;

        // Assert #1
        const link = compiled.querySelector('.btn-solid-invert') as HTMLAnchorElement;

        // Assert #2
        expect(link?.textContent).toContain('Ir al reto');
    });
});
