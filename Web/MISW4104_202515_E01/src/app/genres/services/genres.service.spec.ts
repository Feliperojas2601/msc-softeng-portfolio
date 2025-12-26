/* tslint:disable:no-unused-variable */

import { TestBed } from '@angular/core/testing';
import { GenresService } from './genres.service';
import { provideHttpClient } from '@angular/common/http';

describe('GenresService', () => {
    let service: GenresService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [provideHttpClient()],
        });
        service = TestBed.inject(GenresService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
