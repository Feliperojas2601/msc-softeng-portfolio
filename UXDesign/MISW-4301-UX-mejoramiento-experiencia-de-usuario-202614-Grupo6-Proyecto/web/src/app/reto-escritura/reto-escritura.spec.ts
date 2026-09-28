import { provideRouter } from '@angular/router';
import { RetoEscrituraComponent } from './reto-escritura';
import { ComponentFixture, TestBed } from '@angular/core/testing';

// Test
describe('RetoEscrituraComponent', () => {
    
    // Component
    let fixture: ComponentFixture<RetoEscrituraComponent>;

    // Component under test
    let component: RetoEscrituraComponent;

    // Before each test
    beforeEach(async () => {
        
        // Configure testing module
        await TestBed.configureTestingModule({
            imports: [RetoEscrituraComponent],
            providers: [provideRouter([])],
        }).compileComponents();

        // Rendered HTML
        fixture = TestBed.createComponent(RetoEscrituraComponent);

        // Detect changes
        component = fixture.componentInstance;

        // Detect changes
        fixture.detectChanges();
    });

    // Test #1
    it('should create', () => {
        expect(component).toBeTruthy();
    });

    // Test #2
    it('should not show an error while the typed text still matches the target phrase', () => {
        (component as any).typedText = 'El sol ya salió';
        fixture.detectChanges();
        expect((component as any).hasError).toBe(false);
    });

    // Test #3
    it('should show an error state as soon as the typed text diverges from the target phrase', () => {
        (component as any).typedText = 'El sol ya se fue';
        fixture.detectChanges();
        const compiled = fixture.nativeElement as HTMLElement;
        expect((component as any).hasError).toBe(true);
        expect(compiled.querySelector('.progreso__error')?.textContent).toContain('No coincide');
    });

    // Test #4
    it('should mark the challenge as complete when the typed text matches exactly', () => {
        (component as any).typedText = (component as any).targetPhrase;
        fixture.detectChanges();
        expect((component as any).isComplete).toBe(true);
    });
});
