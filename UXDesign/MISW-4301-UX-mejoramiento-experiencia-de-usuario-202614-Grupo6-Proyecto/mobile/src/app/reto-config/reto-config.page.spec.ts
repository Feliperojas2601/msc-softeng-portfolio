// Librerías
import { RetoConfigPage } from './reto-config.page';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

// Configuración de los tests
describe('RetoConfigPage', () => {

  // Configuración de los tests
  let component: RetoConfigPage;
  let fixture: ComponentFixture<RetoConfigPage>;
  let router: Router;

  // Inicialización de los tests
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RetoConfigPage],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(RetoConfigPage);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  // Validación del componente
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Validación del stepper de pasos (10 a 100)
  it('should clamp the steps between 10 and 100', () => {
    (component as any).alarma.pasosCaminar = 10;
    (component as any).ajustarPasos(-5);
    expect((component as any).alarma.pasosCaminar).toBe(10);

    (component as any).alarma.pasosCaminar = 100;
    (component as any).ajustarPasos(5);
    expect((component as any).alarma.pasosCaminar).toBe(100);
  });

  // Validación de navegación al guardar
  it('should reset the draft and navigate to /alarmas-lista on save', () => {
    const spy = vi.spyOn(router, 'navigate');
    (component as any).alarma.pasosCaminar = 75;
    (component as any).onGuardar();
    expect((component as any).alarma.pasosCaminar).toBe(40);
    expect(spy).toHaveBeenCalledWith(['/alarmas-lista']);
  });
});
