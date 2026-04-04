import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from "@angular/forms";
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Reserva } from '../reserva';
import { ReservaService } from '../reserva.service';
import { ErrorService } from 'src/app/error.service';
import { EncabezadoComponent } from '../../encabezado-app/encabezado/encabezado.component';

@Component({
  selector: 'app-reserva-crear',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, EncabezadoComponent],
  templateUrl: './reserva-crear.component.html',
  styleUrls: ['./reserva-crear.component.css']
})
export class ReservaCrearComponent implements OnInit {

  reservaForm: FormGroup;
  idPropiedad: number;

  constructor(
    private formBuilder: FormBuilder,
    private routerPath: Router,
    private router: ActivatedRoute,
    private toastr: ToastrService,
    private reservaService: ReservaService,
    private errorService: ErrorService
  ) { }

  ngOnInit() {
    this.idPropiedad = parseInt(this.router.snapshot.params['id']);
    this.reservaForm = this.formBuilder.group({
      nombre: ["", [Validators.required, Validators.minLength(2)]],
      fecha_ingreso: ["", [Validators.required, Validators.minLength(2)]],
      fecha_salida: ["", [Validators.required, Validators.minLength(2)]],
      comision: ["", Validators.required],
      total_reserva: ["", Validators.required],
      plataforma_reserva: ["", [Validators.required, Validators.minLength(2)]],
      numero_personas: [],
      observaciones: []
      });
  }

  crearReserva(reserva: Reserva): void {
    this.reservaService.crearReserva(reserva, this.idPropiedad).subscribe((reserva) => {
      this.toastr.success("Confirmation", "Registro creado")
      this.reservaForm.reset();
      this.routerPath.navigate(['/propiedades/' + this.idPropiedad + '/reservas']);
    },
    error => this.errorService.manejarError(error))

  }

  cancelarCrearReserva(): void {
    this.reservaForm.reset();
    this.routerPath.navigate(['/propiedades/' + this.idPropiedad + '/reservas']);
  }

}
