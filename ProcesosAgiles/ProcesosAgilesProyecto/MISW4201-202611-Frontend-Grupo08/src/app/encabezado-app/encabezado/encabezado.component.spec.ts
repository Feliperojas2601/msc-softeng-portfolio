import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EncabezadoComponent } from './encabezado.component';
import { provideRouter, RouterLink, RouterLinkActive } from '@angular/router';

describe('EncabezadoComponent', () => {
    let component: EncabezadoComponent;
    let fixture: ComponentFixture<EncabezadoComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({            
            providers: [provideRouter([])],
            imports: [EncabezadoComponent, RouterLink, RouterLinkActive]
        }).compileComponents();
        fixture = TestBed.createComponent(EncabezadoComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
