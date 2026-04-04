export class Propiedad {
    id: number;
    nombre_propiedad: string;
    ciudad: string;
    municipio: string;
    direccion: string;
    nombre_propietario: string;
    numero_contacto: string;
    banco: string;
    numero_cuenta: string;

    public constructor(id: number, nombre_propiedad: string, ciudad: string, municipio: string, direccion: string,
        nombre_propietario: string, numero_contacto: string, banco: string, numero_cuenta: string) {
        this.id = id;
        this.nombre_propiedad = nombre_propiedad;
        this.ciudad = ciudad;
        this.municipio = municipio;
        this.direccion = direccion;
        this.nombre_propietario = nombre_propietario;
        this.numero_contacto = numero_contacto;
        this.banco = banco;
        this.numero_cuenta = numero_cuenta;
    }
}
