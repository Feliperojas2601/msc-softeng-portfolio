import { forkJoin } from 'rxjs';
import { Banco } from 'src/app/enums';
import { Propiedad } from '../propiedad';
import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { EnumsService } from 'src/app/enums.service';
import { ErrorService } from 'src/app/error.service';
import { PropiedadService } from '../propiedad.service';
import { Component, OnInit, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from "@angular/forms";

@Component({
  selector: 'app-propiedad-editar',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './propiedad-editar.component.html',
  styleUrls: ['./propiedad-editar.component.css']
})
export class PropiedadEditarComponent implements OnInit {
  
  propiedad: Propiedad;
  propiedadForm: FormGroup;
  listaBancos: Banco[] = [];
  @Input() idPropiedad!: number;
  listaPropietarios: {id: number, usuario: string}[] = [];

  constructor(
    private formBuilder: FormBuilder,
    private toastr: ToastrService,
    private propiedadService: PropiedadService,
    private enumService: EnumsService,
    private errorService: ErrorService,
    public activeModal: NgbActiveModal,
  ) {
    this.propiedadForm = this.formBuilder.group({
      nombre_propiedad: ["", Validators.required],
      ciudad: ["", Validators.required],
      municipio: ["", Validators.required],
      direccion: ["", Validators.required],
      nombre_propietario: ["", Validators.required],
      numero_contacto: ["", Validators.required],
      banco: ["", Validators.required],
      numero_cuenta: ["", Validators.required]
    });
   }

  ngOnInit() {    

    forkJoin({
      bancos: this.enumService.bancos(),
      propietarios: this.propiedadService.darPropietarios(),
      propiedad: this.propiedadService.darPropiedad(this.idPropiedad)
    }).subscribe({
      next: ({ bancos, propietarios, propiedad }) => {
        this.listaBancos = bancos;
        this.listaPropietarios = propietarios;
        this.propiedad = propiedad;

        // Precargamos los valores existentes en el formulario
        this.propiedadForm.patchValue({
          nombre_propiedad: propiedad.nombre_propiedad,
          ciudad: propiedad.ciudad,
          municipio: propiedad.municipio,
          direccion: propiedad.direccion,
          nombre_propietario: propiedad.nombre_propietario,
          numero_contacto: propiedad.numero_contacto,
          banco: propiedad.banco,
          numero_cuenta: propiedad.numero_cuenta
        });
      },
      error: () => this.toastr.error('Error al cargar los datos de la propiedad')
    });
  }

  editar(): void {
    // Si el formulario no es válido, mostramos los errores visualmente
    if (this.propiedadForm.invalid) {
      this.propiedadForm.markAllAsTouched();
      return;
    }

    this.propiedadService.editarPropiedad(this.propiedadForm.value, this.idPropiedad).subscribe({
      next: () => {
        this.toastr.success('Propiedad actualizada correctamente');
        this.activeModal.close(true);
      },
      error: (error) => {
        this.toastr.error('Error al actualizar la propiedad');
        this.errorService.manejarError(error);
      }
    });
  }

  cancelar(): void {
    // Cierra el modal sin recargar la lista
    this.activeModal.dismiss();
  }

}
