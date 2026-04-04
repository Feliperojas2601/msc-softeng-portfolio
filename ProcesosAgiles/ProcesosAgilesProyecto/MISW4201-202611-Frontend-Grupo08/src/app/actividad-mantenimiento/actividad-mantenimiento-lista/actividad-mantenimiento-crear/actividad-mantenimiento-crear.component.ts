import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { EstadoMantenimiento, PeriodicidadMantenimiento, TipoCategoriaMantenimiento} from 'src/app/enums';
import { CommonModule } from '@angular/common';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ActividadMantenimiento } from '../../actividad-mantenimiento';
import { Component, OnInit, Input, ViewChild, TemplateRef } from '@angular/core';
import { ActividadMantenimientoService } from '../../actividad-mantenimiento.service';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { EnumsService } from 'src/app/enums.service';

@Component({
  standalone: true,
  selector: 'app-actividad-mantenimiento-crear',
  templateUrl: './actividad-mantenimiento-crear.component.html',
  styleUrls: ['./actividad-mantenimiento-crear.component.css'],
  imports: [CommonModule, ReactiveFormsModule]
})
export class ActividadMantenimientoCrearComponent implements OnInit {
  estados: Array<EstadoMantenimiento>;
  categoriaMantenimientos: Array<TipoCategoriaMantenimiento>;
  periodicidades: Array<PeriodicidadMantenimiento>;
  actividadForm: FormGroup;
  @Input() idPropiedad!: number;
  actividades: ActividadMantenimiento[] = [];
  nombreActividadReciente: string = '';
  @Input() actividadExistente?: ActividadMantenimiento;
  @ViewChild('modalExito') modalExito!: TemplateRef<any>;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    public modalService: NgbModal,
    private toastr: ToastrService,
    public activeModal: NgbActiveModal,
    private actividadService: ActividadMantenimientoService,
    private enumService: EnumsService
  ) {
    this.actividadForm = this.formBuilder.group({
      concepto: ["", [Validators.required]],
      categoria: [null, []],
      periodicidad: ["", [Validators.required, Validators.maxLength(40)]],
      estado: [null, []],
      fecha_registro: [new Date().toISOString().split('T')[0], [Validators.required]],
      costo: ["", [Validators.required, Validators.maxLength(80)]]
    });
   }

  ngOnInit(): void {

        this.enumService.estadoMantenimiento().subscribe((estados) => {
                this.estados = estados;

            this.enumService.tipoCategoriaMantenimiento().subscribe((categoriaMantenimientos) => {
                this.categoriaMantenimientos = categoriaMantenimientos;

                this.enumService.periodicidadMantenimiento().subscribe((periodicidades) => {
                    this.periodicidades = periodicidades;

                    this.actividadForm = this.formBuilder.group({
                        concepto: ["", [Validators.required]],
                        categoria: [null, []],
                        periodicidad: [null, [Validators.required]],
                        estado: [null, []],
                        fecha_registro: [new Date().toISOString().split('T')[0], [Validators.required]],
                        costo: ["", [Validators.required, Validators.maxLength(80)]]
                    });
                });
            });
        
        });
    
        if (this.actividadExistente) {
            this.actividadForm.patchValue(this.actividadExistente);
        }
  }

  obtenerActividades() {
        this.actividadService.darActividadesMantenimiento(this.idPropiedad).subscribe({
            next: (res) => this.actividades = res,
            error: (err) => this.toastr.error(`Error {${err.statusText}} al cargar la lista`)
        });
  }

  mostrarAvisoExito(nombre: string) {

        // Guardamos el nombre del actividad recién creado
        this.nombreActividadReciente = nombre;

        // Presentación del modal
        const modalRef = this.modalService.open(this.modalExito, { centered: true, size: 'sm' });

        // Redirigir al menú de actividades de la propiedad
        modalRef.result.then(() => {

            // Navegación a la propiedad
            this.router.navigate(['/propiedades', this.idPropiedad, '/actividades']);

            // Refrescar la vista o limpiar estados:
            this.obtenerActividades();

        }).catch(() => {

            // Por si cierran con la X o ESC
            this.obtenerActividades();
        });
    }

    guardar(): void {
        console.log("Datos enviados a Flask:", this.actividadForm.value);
        if (this.actividadForm.invalid) return;

        this.actividadService.crearActividadMantenimiento(this.idPropiedad, this.actividadForm.value).subscribe({
            next: (res) => {
                this.toastr.success("Actividad registrada");
                this.activeModal.close(res);
                this.mostrarAvisoExito(res.concepto);
            },
            error: (err) => {
                console.error("Error en Flask:", err);
                this.toastr.error("Error al registrar el actividad");
            }
        });
    }

}
