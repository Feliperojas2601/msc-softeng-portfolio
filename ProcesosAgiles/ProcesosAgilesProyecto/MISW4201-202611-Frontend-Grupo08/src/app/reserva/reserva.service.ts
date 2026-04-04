import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment'
import { Reserva } from './reserva';

@Injectable({
  providedIn: 'root'
})
export class ReservaService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }

  obtenerReservas(id_propiedad: number): Observable<Reserva[]> {
    return this.http.get<Reserva[]>(`${this.apiUrl}/propiedades/${id_propiedad}/reservas`)
  }

  obtenerReserva(id: number): Observable<Reserva> {
    return this.http.get<Reserva>(`${this.apiUrl}/reservas/${id}`)
  }

  crearReserva(reserva: Reserva, id_propiedad: number): Observable<Reserva> {
    return this.http.post<Reserva>(`${this.apiUrl}/propiedades/${id_propiedad}/reservas`, reserva)
  }

  editarReserva(reserva: Reserva, id_reserva: number): Observable<Reserva> {
    return this.http.put<Reserva>(`${this.apiUrl}/reservas/${id_reserva}`, reserva)
  }

  borrarReserva(idReserva: number): Observable<Reserva> {
    return this.http.delete<Reserva>(`${this.apiUrl}/reservas/${idReserva}`)
  }

}
