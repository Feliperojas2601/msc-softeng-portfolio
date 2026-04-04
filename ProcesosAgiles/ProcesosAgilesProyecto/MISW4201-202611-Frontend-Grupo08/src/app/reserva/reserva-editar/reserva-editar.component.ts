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
  selector: 'app-reserva-editar',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, EncabezadoComponent],
  templateUrl: './reserva-editar.component.html',
  styleUrls: ['./reserva-editar.component.css']
})
export class ReservaEditarComponent implements OnInit {

  reserva: Reserva
  reservaForm: FormGroup = {} as FormGroup
  idPropiedad: number
  idReserva: number

  constructor(
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService,
    private reservaService: ReservaService,
    private errorService: ErrorService
  ) {
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

  ngOnInit() {
    this.idReserva = parseInt(this.router.snapshot.params['id_reserva']);
    this.reservaService.obtenerReserva(this.idReserva).subscribe((reserva) => {
      this.reserva = reserva;
      this.reservaForm = this.formBuilder.group({
        nombre: [this.reserva.nombre, [Validators.required, Validators.minLength(2)]],
        fecha_ingreso: [this.reserva.fecha_ingreso, [Validators.required, Validators.minLength(2)]],
        fecha_salida: [this.reserva.fecha_salida, [Validators.required, Validators.minLength(2)]],
        comision: [Number(this.reserva.comision), Validators.required],
        total_reserva: [Number(this.reserva.total_reserva), Validators.required],
        plataforma_reserva: [this.reserva.plataforma_reserva, [Validators.required, Validators.minLength(2)]],
        numero_personas: [this.reserva.numero_personas],
        observaciones: [this.reserva.observaciones]
        });
    });
  }

  editarReserva(reserva: Reserva): void {
    this.reservaService.editarReserva(reserva, this.idReserva).subscribe((reserva) => {
      this.toastr.success("Confirmation", "Información editada")
      this.reservaForm.reset();
      this.routerPath.navigate(['/propiedades/' + this.reserva.id_propiedad + '/reservas']);
    },
    error => this.errorService.manejarError(error))
}

  cancelarEditarReserva(): void {
    this.reservaForm.reset();
    this.routerPath.navigate(['/propiedades/' + this.reserva.id_propiedad + '/reservas']);
  }


}
