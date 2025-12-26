import { TestBed, ComponentFixture } from '@angular/core/testing';
import { FooterComponent } from './footer.component';

describe('FooterComponent', () => {
    let fixture: ComponentFixture<FooterComponent>;
    let component: FooterComponent;
    let compiled: HTMLElement;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [FooterComponent],
        });
        fixture = TestBed.createComponent(FooterComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should display the copyright text', () => {
        const paragraph = compiled.querySelector('p');
        expect(paragraph?.textContent).toContain('© 2025 CineLovers');
        expect(paragraph?.textContent).toContain('Proyecto Académico');
    });

    it('should render the footer element', () => {
        const footer = compiled.querySelector('footer.footer');
        expect(footer).toBeTruthy();
    });

    it('should have centered text', () => {
        const paragraph = compiled.querySelector('p');
        expect(paragraph?.classList.contains('text-center')).toBe(true);
    });
});
