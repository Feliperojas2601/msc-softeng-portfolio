// Libraries
import { provideRouter } from '@angular/router';
import { RetoCompletadoComponent } from './reto-completado';
import { ComponentFixture, TestBed } from '@angular/core/testing';

// Test
describe('RetoCompletadoComponent', () => {
    
    // Component
    let fixture: ComponentFixture<RetoCompletadoComponent>;

    // Before each test
    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [RetoCompletadoComponent],
            providers: [provideRouter([])],
        }).compileComponents();

        // Rendered HTML
        fixture = TestBed.createComponent(RetoCompletadoComponent);
        
        // Detect changes
        fixture.detectChanges();
    });

    // Test #1
    it('should create', () => {
        expect(fixture.componentInstance).toBeTruthy();
    });

    // Test #2
    it('should render a link back to the dashboard', () => {
        const compiled = fixture.nativeElement as HTMLElement;
        const link = compiled.querySelector('.cta-dashboard') as HTMLAnchorElement;
        expect(link?.textContent).toContain('Ir al dashboard');
    });
});
