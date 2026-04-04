export class Movimiento {
    id: number;
    id_reserva: number;
    id_propiedad: number;
    id_categoria: number;
    valor: number;
    fecha: Date;
    tipo_movimiento: string;
    concepto: string;
    categoria: string;

    public constructor(id: number, id_reserva: number, id_propiedad: number, id_categoria: number, valor: number, fecha: Date,
        tipo_movimiento: string, concepto: string, categoria: string) {
            this.id = id;
            this.id_reserva = id_reserva;
            this.id_propiedad = id_propiedad;
            this.id_categoria = id_categoria;
            this.valor = valor;
            this.fecha = fecha;
            this.tipo_movimiento = tipo_movimiento;
            this.concepto = concepto;
            this.categoria = categoria;
        }
}
