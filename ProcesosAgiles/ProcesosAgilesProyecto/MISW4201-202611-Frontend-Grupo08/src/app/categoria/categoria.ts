export class Categoria {
    id: number;
    nombre: string;
    id_usuario: number;

    public constructor(id: number, nombre: string, id_usuario: number) {
        this.id = id;
        this.nombre = nombre;
        this.id_usuario = id_usuario;
    }
}