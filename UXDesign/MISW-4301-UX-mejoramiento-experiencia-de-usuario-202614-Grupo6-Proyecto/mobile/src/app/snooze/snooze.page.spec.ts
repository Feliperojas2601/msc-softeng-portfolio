// Librerías
import { SnoozePage } from './snooze.page';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

// Configuración de los tests
describe('SnoozePage', () => {

  // Configuración de los tests
  let component: SnoozePage;
  let fixture: ComponentFixture<SnoozePage>;
  let router: Router;

  // Inicialización de los tests
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SnoozePage],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(SnoozePage);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  // Validación del componente
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Validación de selección de duración
  it('should select a duration chip', () => {
    (component as any).seleccionarDuracion('15 min');
    expect((component as any).alarma.duracionSeleccionada).toBe('15 min');
  });

  // Validación del límite de posposiciones (0 a 5)
  it('should clamp the posposition limit between 0 and 5', () => {
    (component as any).alarma.limitePosposiciones = 5;
    (component as any).ajustarLimite(1);
    expect((component as any).alarma.limitePosposiciones).toBe(5);

    (component as any).alarma.limitePosposiciones = 0;
    (component as any).ajustarLimite(-1);
    expect((component as any).alarma.limitePosposiciones).toBe(0);
  });

  // Validación de navegación
  it('should navigate to /reto-config on continue', () => {
    const spy = vi.spyOn(router, 'navigate');
    (component as any).onContinuar();
    expect(spy).toHaveBeenCalledWith(['/reto-config']);
  });
});
