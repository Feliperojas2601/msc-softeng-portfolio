import { Observable} from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '../../environments/environment'

@Injectable({providedIn: 'root'})

export class UsuarioService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, { "username": username, "password": password });
  }

  registro(username: string, role: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/signin`, { "username": username, "role": role, "password": password })  }

}
