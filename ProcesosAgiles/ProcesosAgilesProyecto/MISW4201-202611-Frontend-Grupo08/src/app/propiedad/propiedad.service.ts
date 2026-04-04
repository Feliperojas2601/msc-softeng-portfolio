import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment'
import { Propiedad } from './propiedad';

@Injectable({
  providedIn: 'root'
})
export class PropiedadService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }


  darPropiedades(): Observable<Propiedad[]> {
    return this.http.get<Propiedad[]>(`${this.apiUrl}/propiedades`)
  }

  darPropiedad(idPropiedad: number): Observable<Propiedad> {
    return this.http.get<Propiedad>(`${this.apiUrl}/propiedades/${idPropiedad}`)
  }

  crearPropiedad(propiedad: Propiedad): Observable<Propiedad> {
    return this.http.post<Propiedad>(`${this.apiUrl}/propiedades`, propiedad);
  }

  editarPropiedad(propiedad: Propiedad, idPropiedad: number): Observable<Propiedad> {
    return this.http.put<Propiedad>(`${this.apiUrl}/propiedades/${idPropiedad}`, propiedad)
  }

  borrarPropiedad(idPropiedad: number): Observable<Propiedad> {
    return this.http.delete<Propiedad>(`${this.apiUrl}/propiedades/${idPropiedad}`)
  }

  darPropietarios(): Observable<{id: number, usuario: string}[]> {
    return this.http.get<{id: number, usuario: string}[]>(`${this.apiUrl}/propietarios`)
  }

}
