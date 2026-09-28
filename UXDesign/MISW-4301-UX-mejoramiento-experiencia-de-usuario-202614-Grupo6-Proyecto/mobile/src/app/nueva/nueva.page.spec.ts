// Librerías
import { NuevaPage } from './nueva.page';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Router } from '@angular/router';

// Configuración de los tests
describe('NuevaPage', () => {

  // Configuración de los tests
  let component: NuevaPage;
  let fixture: ComponentFixture<NuevaPage>;
  let router: Router;

  // Inicialización de los tests
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NuevaPage],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(NuevaPage);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  // Validación del componente
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Validación de días
  it('should toggle a day chip', () => {
    const dia = (component as any).alarma.dias[0];
    const initial = dia.active;
    (component as any).toggleDia(dia);
    expect(dia.active).toBe(!initial);
  });

  // Validación de navegación
  it('should navigate to /snooze on continue', () => {
    const spy = vi.spyOn(router, 'navigate');
    (component as any).onContinuar();
    expect(spy).toHaveBeenCalledWith(['/snooze']);
  });
});
