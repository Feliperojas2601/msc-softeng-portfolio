import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Reserva } from '../reserva';
import { ReservaService } from '../reserva.service';
import { ErrorService } from 'src/app/error.service';
import { EncabezadoComponent } from '../../encabezado-app/encabezado/encabezado.component';

@Component({
  selector: 'app-reserva-lista',
  standalone: true,
  imports: [CommonModule, EncabezadoComponent],
  templateUrl: './reserva-lista.component.html',
  styleUrls: ['./reserva-lista.component.css']
})
export class ReservaListaComponent implements OnInit {

  reservas:Array<Reserva> = []
  idPropiedad: number;

  constructor(
    private routerPath: Router,
    private router: ActivatedRoute,
    private toastr: ToastrService,
    private reservaService: ReservaService,
    private errorService: ErrorService
  ) { }

  ngOnInit() {
    this.idPropiedad = parseInt(this.router.snapshot.params['id']);
    this.reservaService.obtenerReservas(this.idPropiedad).subscribe((reservas) => {
      this.reservas = reservas;
    })
  }

  crearReserva():void {
    this.routerPath.navigate(['propiedades/' + this.idPropiedad + '/reserva/crear/']);
  }

  editarReserva(idReserva: number):void {
    this.routerPath.navigate(['propiedades/' + this.idPropiedad + '/reserva/editar/' + idReserva]);
  }

  borrarReserva(idReserva: number):void {
    this.reservaService.borrarReserva(idReserva).subscribe(() => {
      this.toastr.success("Confirmation", "Registro eliminado de la lista")
      this.ngOnInit();
    },
    error => this.errorService.manejarError(error));
  }
}
