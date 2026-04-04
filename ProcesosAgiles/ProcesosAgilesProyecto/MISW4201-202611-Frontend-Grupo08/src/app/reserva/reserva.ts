export class Reserva {
  id: number;
  fecha_ingreso: Date;
  fecha_salida: Date;
  plataforma_reserva: string;
  total_reserva: number;
  comision: number;
  nombre: string;
  id_propiedad: number;
  observaciones: string;
  numero_personas: number;

  public constructor(id: number, fecha_ingreso: Date, fecha_salida: Date, plataforma_reserva: string, total_reserva: number, comision: number,
    nombre: string, id_propiedad: number, numero_personas: number, observaciones: string) {
    this.id = id;
    this.nombre = nombre;
    this.fecha_ingreso = fecha_ingreso;
    this.fecha_salida = fecha_salida;
    this.plataforma_reserva = plataforma_reserva;
    this.total_reserva = total_reserva;
    this.comision = comision;
    this.id_propiedad = id_propiedad;
    this.numero_personas = numero_personas;
    this.observaciones = observaciones;
  }
}
