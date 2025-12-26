import { TestBed, ComponentFixture } from '@angular/core/testing';
import { LoaderComponent } from './loader.component';

describe('LoaderComponent', () => {
    let fixture: ComponentFixture<LoaderComponent>;
    let component: LoaderComponent;
    let compiled: HTMLElement;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [LoaderComponent],
        });
        fixture = TestBed.createComponent(LoaderComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should display the loading message with the item name', () => {
        fixture.componentRef.setInput('item', 'actores');
        fixture.detectChanges();
        const paragraph = compiled.querySelector('p');
        expect(paragraph?.textContent).toContain('Cargando actores...');
    });

    it('should render the spinner', () => {
        fixture.componentRef.setInput('item', 'datos');
        fixture.detectChanges();
        const spinner = compiled.querySelector('.spinner-border');
        expect(spinner).toBeTruthy();
        expect(spinner?.classList.contains('text-primary')).toBe(true);
    });
});
