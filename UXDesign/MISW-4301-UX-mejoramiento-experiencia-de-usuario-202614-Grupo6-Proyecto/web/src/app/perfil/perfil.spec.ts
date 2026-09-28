import { PerfilComponent } from './perfil';
import { provideRouter } from '@angular/router';
import { ComponentFixture, TestBed } from '@angular/core/testing';

// Test
describe('PerfilComponent', () => {
  
  // Component
  let component: PerfilComponent;
  let fixture: ComponentFixture<PerfilComponent>;

  // Before each test
  beforeEach(async () => {
    
    // Configure testing module
    await TestBed.configureTestingModule({
      imports: [PerfilComponent],
      providers: [provideRouter([])], 
    }).compileComponents();

    // Rendered HTML
    fixture = TestBed.createComponent(PerfilComponent);
    
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
  it('should render the page title "Perfil"', () => {
    const title: HTMLElement = fixture.nativeElement.querySelector('.topbar__title');
    expect(title?.textContent).toContain('Perfil');
  });

  // Test #3
  it('should render the user name in the account card', () => {    
    const nombre: HTMLElement = fixture.nativeElement.querySelector('.cuenta__nombre');
    expect(nombre?.textContent).toContain('Paula Alarcón');
  });

  // Test #4
  it('should render exactly 3 preference rows', () => {
    const filas: NodeListOf<HTMLElement> = fixture.nativeElement.querySelectorAll('.preferencia');
    expect(filas.length).toBe(3);
  });

  // Test #5
  it('should render exactly 2 emergency exit entries', () => {
    const salidas: NodeListOf<HTMLElement> = fixture.nativeElement.querySelectorAll('.emergencia__item');
    expect(salidas.length).toBe(2);
  });

  // Test #6
  it('should mark "Perfil" as the active nav item', () => {
    const activo: HTMLElement = fixture.nativeElement.querySelector('.nav-item--active');
    expect(activo?.textContent).toContain('Perfil');
  });
});
