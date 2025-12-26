import { TestBed, ComponentFixture } from '@angular/core/testing';
import { NavbarComponent } from './navbar.component';
import { provideRouter } from '@angular/router';

describe('NavbarComponent', () => {
    let fixture: ComponentFixture<NavbarComponent>;
    let component: NavbarComponent;
    let compiled: HTMLElement;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [NavbarComponent],
            providers: [provideRouter([])],
        });
        fixture = TestBed.createComponent(NavbarComponent);
        component = fixture.componentInstance;
        compiled = fixture.nativeElement;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should render all navigation links', () => {
        const navLinks = compiled.querySelectorAll('.nav-link');
        expect(navLinks.length).toBe(6);
    });

    it('should have the correct navigation items', () => {
        const navLinks = compiled.querySelectorAll('.nav-link');
        const navTexts = Array.from(navLinks).map((link) =>
            link.textContent?.trim(),
        );

        expect(navTexts).toContain('Inicio');
        expect(navTexts).toContain('Películas');
        expect(navTexts).toContain('Actores');
        expect(navTexts).toContain('Directores');
        expect(navTexts).toContain('Géneros');
        expect(navTexts).toContain('Plataformas');
    });

    it('should have navbar element with correct class', () => {
        const navbar = compiled.querySelector('nav.navbar');
        expect(navbar).toBeTruthy();
        expect(navbar?.classList.contains('navbar-expand-lg')).toBe(true);
    });

    it('should render the navbar toggler button for mobile', () => {
        const togglerButton = compiled.querySelector('.navbar-toggler');
        expect(togglerButton).toBeTruthy();
    });
});
