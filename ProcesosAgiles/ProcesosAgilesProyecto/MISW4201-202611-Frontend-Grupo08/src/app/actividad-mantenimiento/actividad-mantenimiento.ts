export class ActividadMantenimiento {
    id: number;
    concepto: string;
    categoria: string;
    periodicidad: string;
    estado: string;
    fecha_registro: string;
    costo: number;
    id_propiedad: number;

    public constructor(id: number, concepto: string, categoria: string, periodicidad: string, estado: string,fecha_registro: string, costo: number, id_propiedad: number) {
        this.id = id;
        this.concepto = concepto;
        this.categoria = categoria;
        this.periodicidad = periodicidad;
        this.estado = estado;
        this.fecha_registro = fecha_registro;
        this.costo = costo;
        this.id_propiedad = id_propiedad;
    }
}