export class ElementoPropiedad {
    id: number;
    nombre: string;
    tipo: string;
    estado: string;
    descripcion: string;
    fecha_registro: string;
    zona: string;
    id_propiedad: number;

    public constructor(id: number, nombre: string, tipo: string, estado: string, descripcion: string,fecha_registro: string, zona: string, id_propiedad: number) {
        this.id = id;
        this.nombre = nombre;
        this.tipo = tipo;
        this.estado = estado;
        this.descripcion = descripcion;
        this.fecha_registro = fecha_registro;
        this.zona = zona;
        this.id_propiedad = id_propiedad;
    }
}