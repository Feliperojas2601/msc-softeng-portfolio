// Librerías
import { AlarmasListaPage } from './alarmas-lista.page';
import { beforeEach, describe, expect, it } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

// Configuración de los tests
describe('AlarmasListaPage', () => {

  // Configuración de los tests
  let component: AlarmasListaPage;
  let fixture: ComponentFixture<AlarmasListaPage>;

  // Inicialización de los tests
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlarmasListaPage],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(AlarmasListaPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // Validación del componente
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Validación de la lista de alarmas
  it('should render both mock alarms', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const items = compiled.querySelectorAll('.item-alarma');
    expect(items.length).toBe(2);
  });

  // Validación del switch
  it('should toggle an alarm active state on click', () => {
    const alarma = (component as any).alarmas[0];
    const initial = alarma.activa;
    (component as any).toggleAlarma(alarma);
    expect(alarma.activa).toBe(!initial);
  });
});
