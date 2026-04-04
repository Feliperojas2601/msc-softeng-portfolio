import { Observable } from 'rxjs';
import { Categoria } from './categoria';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class CategoriaService {
    // URL de la API
    private apiUrl = environment.apiUrl;
    
    // Constructor
    constructor(private http: HttpClient) { }
    
    // Obtener lista de categorias
    private getHeaders(): HttpHeaders {
        
        // Obtenemos el token de la sesión
        const token = localStorage.getItem('token');

        // Creamos las cabeceras necesarias para la petición
        return new HttpHeaders({ 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`});
    }

    // GET /categorias
    darCategorias(): Observable<Categoria[]> {
        
        // Retornamos la lista de categorias
        return this.http.get<Categoria[]>(`${this.apiUrl}/categorias`, { headers: this.getHeaders() });
    }

    // POST /categorias
    crearCategoria(nombre: String): Observable<Categoria> {

        // Retornamos la nueva categoria
        return this.http.post<Categoria>(`${this.apiUrl}/categorias`, { nombre }, { headers: this.getHeaders() });
    }

    // PUT /categorias/:id
    editarCategoria(id: number, nombre: String): Observable<Categoria> {

        // Retornamos la nueva categoria
        return this.http.put<Categoria>(`${this.apiUrl}/categorias/${id}`, { nombre }, { headers: this.getHeaders() });
    }

    // DELETE /categorias/:id
    eliminarCategoria(id: number): Observable<Categoria> {

        // Retornamos la nueva categoria
        return this.http.delete<Categoria>(`${this.apiUrl}/categorias/${id}`, { headers: this.getHeaders() });
    }
}