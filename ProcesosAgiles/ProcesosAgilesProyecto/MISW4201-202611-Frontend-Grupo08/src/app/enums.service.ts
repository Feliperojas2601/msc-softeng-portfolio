import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Banco, TipoMovimiento, TipoCategoria, EstadoMantenimiento, TipoCategoriaMantenimiento, PeriodicidadMantenimiento } from './enums';

@Injectable({
  providedIn: 'root'
})
export class EnumsService {

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  bancos(): Observable<Banco[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/bancos`, { headers: headers });
  }

  tiposMovimiento(): Observable<TipoMovimiento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/tipo-movimientos`, { headers: headers });
  }

  tiposCategoria(): Observable<TipoCategoria[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/tipo-categorias`, { headers: headers });
  }

  estadoMantenimiento(): Observable<EstadoMantenimiento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/estado-mantenimientos`, { headers: headers });
  }

  tipoCategoriaMantenimiento(): Observable<TipoCategoriaMantenimiento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/tipo-categoria-mantenimientos`, { headers: headers });
  }

  periodicidadMantenimiento(): Observable<PeriodicidadMantenimiento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`
    })
    return this.http.get<PeriodicidadMantenimiento[]>(`${this.apiUrl}/periodicidad-mantenimientos`, { headers: headers });
  }

}
