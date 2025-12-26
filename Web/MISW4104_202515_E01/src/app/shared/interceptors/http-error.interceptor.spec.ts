import { TestBed } from '@angular/core/testing';
import { httpErrorInterceptor } from './http-error.interceptor';
import { ToastrService } from 'ngx-toastr';
import {
    HttpClient,
    provideHttpClient,
    withInterceptors,
} from '@angular/common/http';
import {
    HttpTestingController,
    provideHttpClientTesting,
} from '@angular/common/http/testing';

describe('httpErrorInterceptor', () => {
    let httpClient: HttpClient;
    let httpMock: HttpTestingController;
    let toastrService: jasmine.SpyObj<ToastrService>;

    beforeEach(() => {
        const toastrSpy = jasmine.createSpyObj('ToastrService', ['error']);

        TestBed.configureTestingModule({
            providers: [
                provideHttpClient(withInterceptors([httpErrorInterceptor])),
                provideHttpClientTesting(),
                { provide: ToastrService, useValue: toastrSpy },
            ],
        });

        httpClient = TestBed.inject(HttpClient);
        httpMock = TestBed.inject(HttpTestingController);
        toastrService = TestBed.inject(
            ToastrService,
        ) as jasmine.SpyObj<ToastrService>;
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should create', () => {
        expect(httpErrorInterceptor).toBeTruthy();
    });

    it('should handle server error and show toastr message', (done) => {
        const testUrl = '/test';
        const errorMessage = '500: Internal Server Error';

        httpClient.get(testUrl).subscribe({
            next: () => fail('should have failed with 500 error'),
            error: (error) => {
                setTimeout(() => {
                    expect(toastrService.error).toHaveBeenCalledWith(
                        errorMessage,
                        'Server side error',
                        { closeButton: true },
                    );
                    done();
                }, 0);
            },
        });

        const req = httpMock.expectOne(testUrl);
        req.flush('Error', {
            status: 500,
            statusText: 'Internal Server Error',
        });
    });

    it('should handle no connection error and show specific message', (done) => {
        const testUrl = '/test';
        const errorMessage = 'No hay conexión con el servidor';

        httpClient.get(testUrl).subscribe({
            next: () => fail('should have failed with connection error'),
            error: (error) => {
                setTimeout(() => {
                    expect(toastrService.error).toHaveBeenCalledWith(
                        errorMessage,
                        'Server side error',
                        { closeButton: true },
                    );
                    done();
                }, 0);
            },
        });

        const req = httpMock.expectOne(testUrl);
        req.flush('Error', { status: 0, statusText: 'Unknown Error' });
    });
});
