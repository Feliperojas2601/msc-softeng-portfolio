import { Banco } from 'src/app/enums';
import { Propiedad } from '../propiedad';
import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { PropiedadService } from '../propiedad.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from "@angular/forms";
import { EncabezadoComponent } from 'src/app/encabezado-app/encabezado/encabezado.component';

@Component({
  selector: 'app-propiedad-crear',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, EncabezadoComponent],
  templateUrl: './propiedad-crear.component.html',
  styleUrls: ['./propiedad-crear.component.css']
})
export class PropiedadCrearComponent implements OnInit {

  propiedadForm: FormGroup;
  listaBancos: Banco[] = [];
  listaPropietarios: {id: number, usuario: string}[] = [];

  constructor(
    private formBuilder: FormBuilder,
    private toastr: ToastrService,
    private propiedadService: PropiedadService,
    private enumService: EnumsService,
    private errorService: ErrorService,
    public activeModal: NgbActiveModal
  ) {
    this.propiedadForm = this.formBuilder.group({
      nombre_propiedad: ["", Validators.required],
      ciudad: ["", Validators.required],
      municipio: ["", Validators.required],
      direccion: ["", Validators.required],
      nombre_propietario: ["", Validators.required],
      numero_contacto: ["", Validators.required],
      banco: [null, Validators.required],
      numero_cuenta: ["", Validators.required]
    });
  }

  ngOnInit() {

    this.propiedadService.darPropietarios().subscribe({
      next: (propietarios) => {
        this.listaPropietarios = propietarios;
      },
      error: (error) => this.toastr.error("Error al cargar propietarios")
    });

    this.enumService.bancos().subscribe({
      next: (bancos) => {
        this.listaBancos = bancos;
      },
      error: () => this.toastr.error('Error al cargar bancos')
    });

  }

  guardar(): void {
    if (this.propiedadForm.invalid) {
      this.propiedadForm.markAllAsTouched();
      return;
    }

    this.propiedadService.crearPropiedad(this.propiedadForm.value).subscribe({
      next: () => {
        this.toastr.success("Propiedad creada correctamente")
        this.activeModal.close(true);
      },
      error: (error) => {
        this.errorService.manejarError(error);
      }
    });
  }

  cancelar(): void {
    this.activeModal.dismiss();
  }


}
