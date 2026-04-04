import { Observable, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { ElementoPropiedad } from './elemento-propiedad';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class ElementoPropiedadService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }


  darElementosPropiedad(idPropiedad: number): Observable<ElementoPropiedad[]> {
    return this.http.get<ElementoPropiedad[]>(`${this.apiUrl}/propiedades/${idPropiedad}/elementos_propiedad`)
  }

  darElementoPropiedad(idPropiedad: number, idElementoPropiedad: number): Observable<ElementoPropiedad> {
    return this.http.get<ElementoPropiedad>(`${this.apiUrl}/propiedades/${idPropiedad}/elementos_propiedad/${idElementoPropiedad}`)
  }

  crearElementoPropiedad(idPropiedad: number, elementoPropiedad: ElementoPropiedad): Observable<ElementoPropiedad> {
    return this.http.post<ElementoPropiedad>(`${this.apiUrl}/propiedades/${idPropiedad}/elementos_propiedad`, elementoPropiedad)
  }

  editarElementoPropiedad(idPropiedad: number, elementoPropiedad: ElementoPropiedad, idElementoPropiedad: number): Observable<ElementoPropiedad> {
    return this.http.put<ElementoPropiedad>(`${this.apiUrl}/propiedades/${idPropiedad}/elementos_propiedad/${idElementoPropiedad}`, elementoPropiedad)
  }

  borrarElementoPropiedad(idPropiedad: number, idElementoPropiedad: number): Observable<any> {
    return this.http.delete<ElementoPropiedad>(`${this.apiUrl}/propiedades/${idPropiedad}/elementos_propiedad/${idElementoPropiedad}`)
  }

}
