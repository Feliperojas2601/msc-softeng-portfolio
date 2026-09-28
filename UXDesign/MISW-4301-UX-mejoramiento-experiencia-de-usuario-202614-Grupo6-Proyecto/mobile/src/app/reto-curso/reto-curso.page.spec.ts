// Librerías
import { RetoCursoPage } from './reto-curso.page';
import { beforeEach, describe, expect, it } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

// Configuración de los tests
describe('RetoCursoPage', () => {

  // Configuración de los tests
  let component: RetoCursoPage;
  let fixture: ComponentFixture<RetoCursoPage>;

  // Inicialización de los tests
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RetoCursoPage],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(RetoCursoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // Validación del componente
  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
