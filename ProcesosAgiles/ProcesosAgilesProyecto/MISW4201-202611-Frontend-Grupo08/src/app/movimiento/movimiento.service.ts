import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Movimiento } from './movimiento';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MovimientoService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }


  obtenerMovimientos(idPropiedad: number): Observable<Movimiento[]> {
    return this.http.get<Movimiento[]>(`${this.apiUrl}/propiedades/${idPropiedad}/movimientos`);
  }

  obtenerMovimiento(idMovimiento: number): Observable<Movimiento> {
    return this.http.get<Movimiento>(`${this.apiUrl}/movimientos/${idMovimiento}`);
  }

  actualizarMovimiento(movimiento: Movimiento, idMovimiento: number): Observable<Movimiento> {
    return this.http.put<Movimiento>(`${this.apiUrl}/movimientos/${idMovimiento}`, movimiento);
  }

  eliminarMovimiento(idMovimiento: number): Observable<Movimiento> {
    return this.http.delete<Movimiento>(`${this.apiUrl}/movimientos/${idMovimiento}`);
  }

  crearMovimiento(movimiento: Movimiento, idPropiedad: number): Observable<Movimiento> {
    return this.http.post<Movimiento>(`${this.apiUrl}/propiedades/${idPropiedad}/movimientos`, movimiento);
  }

}
