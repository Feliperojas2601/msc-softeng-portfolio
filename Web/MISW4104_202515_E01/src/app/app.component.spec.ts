import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { provideHttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { provideRouter } from '@angular/router';

describe('AppComponent', () => {
    const mockActivatedRoute = {
        snapshot: {
            paramMap: {
                get: (key: string) => 'actors',
            },
        },
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [AppComponent],
            providers: [
                provideHttpClient(),
                provideRouter([]),
                { provide: ActivatedRoute, useValue: mockActivatedRoute },
            ],
        });
    });

    it('should create the app', () => {
        const fixture = TestBed.createComponent(AppComponent);
        const app = fixture.componentInstance;
        expect(app).toBeTruthy();
    });
});
