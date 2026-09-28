import { LoginComponent } from './login';
import { provideRouter } from '@angular/router';
import { ComponentFixture, TestBed } from '@angular/core/testing';

// Test
describe('LoginComponent', () => {
    
    // Component
    let fixture: ComponentFixture<LoginComponent>;

    // Before each test
    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [LoginComponent],
            providers: [provideRouter([])],
        }).compileComponents();

        fixture = TestBed.createComponent(LoginComponent);
        fixture.detectChanges();
    });

    // Test #1
    it('should create', () => {
        expect(fixture.componentInstance).toBeTruthy();
    });

    // Test #2
    it('should render both SSO buttons at full width of the card', () => {
        
        // Rendered HTML
        const compiled = fixture.nativeElement as HTMLElement;

        // Assert # 1
        const buttons = compiled.querySelectorAll('.cta-sso');
        
        // Assert #2
        expect(buttons.length).toBe(2);

        // Assert #3
        expect(buttons[0].textContent).toContain('Continuar con Google');

        // Assert #4
        expect(buttons[1].textContent).toContain('Continuar con Apple');
    });
});
