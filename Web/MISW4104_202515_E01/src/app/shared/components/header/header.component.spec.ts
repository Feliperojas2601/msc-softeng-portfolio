import { TestBed, ComponentFixture } from '@angular/core/testing';
import { HeaderComponent } from './header.component';

describe('HeaderComponent', () => {
    let fixture: ComponentFixture<HeaderComponent>;
    let component: HeaderComponent;
    let compiled: HTMLElement;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HeaderComponent],
        });
        fixture = TestBed.createComponent(HeaderComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should render the logo circle', () => {
        const logoCircle = compiled.querySelector('.logo-circle');
        expect(logoCircle).toBeTruthy();
    });

    it('should display the CineLovers title', () => {
        const logoText = compiled.querySelector('.logo-text');
        expect(logoText?.textContent).toContain('CineLovers');
    });

    it('should have the header element with gradient background', () => {
        const header = compiled.querySelector('header.header');
        expect(header).toBeTruthy();
    });
});
