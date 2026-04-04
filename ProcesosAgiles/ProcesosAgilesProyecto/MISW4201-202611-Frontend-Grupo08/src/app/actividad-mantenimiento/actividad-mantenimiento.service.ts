import { Observable, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { ActividadMantenimiento } from './actividad-mantenimiento';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class ActividadMantenimientoService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }


  darActividadesMantenimiento(idPropiedad: number): Observable<ActividadMantenimiento[]> {
    return this.http.get<ActividadMantenimiento[]>(`${this.apiUrl}/propiedades/${idPropiedad}/actividades_mantenimiento`)
  }

  crearActividadMantenimiento(idPropiedad: number, ActividadMantenimiento: ActividadMantenimiento): Observable<ActividadMantenimiento> {
    return this.http.post<ActividadMantenimiento>(`${this.apiUrl}/propiedades/${idPropiedad}/actividades_mantenimiento`, ActividadMantenimiento)
  }

  editarActividadMantenimiento(idPropiedad: number, idActividad: number, actividad: Partial<ActividadMantenimiento>): Observable<ActividadMantenimiento> {
    return this.http.put<ActividadMantenimiento>(`${this.apiUrl}/propiedades/${idPropiedad}/actividades_mantenimiento/${idActividad}`, actividad)
  }

  eliminarActividadMantenimiento(idPropiedad: number, idActividad: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/propiedades/${idPropiedad}/actividades_mantenimiento/${idActividad}`)
  }

}