export class Banco {

    public constructor() {
    }
}

export class TipoMovimiento {

    public constructor() {
        
    }
}

export class TipoCategoria {

    public constructor() {
        
    }
}

export enum TipoEstado {
    EXCELENTE = "EXCELENTE",
    BUENO = "BUENO",
    REGULAR = "REGULAR",
    MALO = "MALO"
}

export class EstadoMantenimiento{

    public constructor(){

    }
}

export class TipoCategoriaMantenimiento{

    public constructor(){

    }
}

export enum PeriodicidadMantenimiento {
    EVENTO = 'EVENTO',
    MENSUAL = 'MENSUAL',
    TRIMESTRAL = 'TRIMESTRAL'
}