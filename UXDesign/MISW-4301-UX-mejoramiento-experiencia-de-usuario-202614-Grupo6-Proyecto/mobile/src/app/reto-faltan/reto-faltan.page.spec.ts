// Librerías
import { provideRouter } from '@angular/router';
import { RetoFaltanPage } from './reto-faltan.page';
import { beforeEach, describe, expect, it } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';

// Configuración de los tests
describe('RetoFaltanPage', () => {

  // Variables de estado
  let component: RetoFaltanPage;
  let fixture: ComponentFixture<RetoFaltanPage>;

  // Inicialización de los tests
  beforeEach(async () => {
    
    // Await configuración de los tests
    await TestBed.configureTestingModule({
      imports: [RetoFaltanPage],
      providers: [
        provideRouter([]),
      ],
    }).compileComponents();

    // Crear componente
    fixture = TestBed.createComponent(RetoFaltanPage);
    
    // Obtener componente
    component = fixture.componentInstance;
    
    // Detectar cambios
    fixture.detectChanges();
  });

  // Validación del componente
  it('should create', () => {
    expect(component).toBeTruthy();
  });
});