import { Categoria } from '../categoria';
import { ToastrService } from 'ngx-toastr';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CategoriaService } from '../categoria.service';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { Component, OnInit, Input, OnDestroy, ElementRef, HostListener, forwardRef } from '@angular/core';

@Component({
  selector: 'app-categoria-selector',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './categoria-selector.component.html',
  styleUrls: ['./categoria-selector.component.css'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => CategoriaSelectorComponent),
      multi: true
    }
  ]
})
export class CategoriaSelectorComponent implements OnInit, ControlValueAccessor {

  // Valor inicial para modo edición — recibe el id de la categoría actual
  @Input() valorInicial: number | null = null;

  // Lista de categorias cargadas
  categorias: Categoria[] = [];
  categoriasFiltradas: Categoria[] = [];
  categoriaSeleccionada: Categoria | null = null;

  // Variables para el input de búsqueda
  textoBusqueda: string  = '';
  dropdownAbierto = false;
  panelAbierto: 'Agregar' | 'Eliminar' | null = null;
  modoEliminar = false;
  nombreNueva = '';

  @HostListener('document:click', ['$event'])
  onClickFuera(event: Event): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.cerrar();
    }
  }

  // Detecta Tab para cerrar el dropdown
  @HostListener('keydown.tab')
  onTab(): void {
    this.cerrar();
  }

  // ControlValueAccessor
  private onChange: (value: number | null) => void = () => {};
  private onTouched: () => void = () => {};

  constructor(
    private toastr: ToastrService,
    private elementRef: ElementRef,
    private categoriaService: CategoriaService,
  ) {}

  ngOnInit(): void {
    this.categoriaService.darCategorias().subscribe({
      next: (categorias) => {
        this.categorias = categorias;
        this.categoriasFiltradas = categorias;

        // Si viene valorInicial (modo edición), pre-seleccionamos
        if (this.valorInicial) {
          const encontrada = this.categorias.find(c => c.id === this.valorInicial);
          if (encontrada) this.seleccionar(encontrada);
        }
      },
      error: () => this.toastr.error('Error al cargar categorías')
    });
  }

  
  abrir(): void {
    this.dropdownAbierto = true;
    this.filtrar('');
  }

  cerrar(): void {
    this.dropdownAbierto = false;
    this.panelAbierto = null;
    this.modoEliminar = false;
    this.nombreNueva = '';
    this.textoBusqueda = this.categoriaSeleccionada?.nombre ?? '';
    this.onTouched();
  }

  filtrar(valor: string): void {
    this.categoriasFiltradas = this.categorias.filter(c =>
      c.nombre.toLowerCase().includes(valor.toLowerCase())
    );
    this.dropdownAbierto = true;
  }

  
  togglePanel(modo: 'agregar' | 'eliminar'): void {
    if (modo === 'agregar') {
      const estaAbierto = this.panelAbierto === 'Agregar';
      this.panelAbierto = estaAbierto ? null : 'Agregar';
      this.modoEliminar = false;
    } else {
      this.modoEliminar = !this.modoEliminar;
      this.panelAbierto = null;
    }
  }

  seleccionar(categoria: Categoria): void {
    if (this.modoEliminar) return;
    this.categoriaSeleccionada = categoria;
    this.textoBusqueda = categoria.nombre;
    this.onChange(categoria.id);
    this.cerrar();
  }

  limpiarSeleccion(): void {
    this.categoriaSeleccionada = null;
    this.textoBusqueda = '';
    this.onChange(null);
  }

  crearCategoria(): void {
    const nombre = this.nombreNueva.trim();
    if (!nombre) return;

    this.categoriaService.crearCategoria(nombre).subscribe({
      next: (nueva) => {
        this.categorias.push(nueva);
        this.filtrar('');
        this.seleccionar(nueva);
        this.nombreNueva = '';
        this.panelAbierto = null;
        this.toastr.success(`Categoría "${nueva.nombre}" creada`);
      },
      error: (err) => {
        const mensaje = err.error?.mensaje ?? `Error al crear la categoría "${nombre}"`;
        this.toastr.error(mensaje);
      }
    });
  }

  eliminarCategoria(categoria: Categoria, event: Event): void {
    event.stopPropagation();

    this.categoriaService.eliminarCategoria(categoria.id).subscribe({
      next: () => {
        this.categorias = this.categorias.filter(c => c.id !== categoria.id);
        this.filtrar(this.textoBusqueda);
        if (this.categoriaSeleccionada?.id === categoria.id) this.limpiarSeleccion();
        this.toastr.success(`Categoría "${categoria.nombre}" eliminada`);
      },
      error: (err) => {
        const mensaje = err.error?.mensaje ?? `Error al eliminar la categoría "${categoria.nombre}"`;
        this.toastr.error(mensaje);
      }
    });
  }

  writeValue(value: number | null): void {
    if (value && this.categorias.length) {
      const encontrada = this.categorias.find(c => c.id === value);
      if (encontrada) this.seleccionar(encontrada);
    }
  }

  registerOnChange(fn: (value: number | null) => void): void { this.onChange = fn; }
  registerOnTouched(fn: () => void): void { this.onTouched = fn; }
}