from dataclasses import dataclass
from typing import Generic, Optional, Tuple, TypeVar
from sqlalchemy import select
from modelos import Propiedad, Reserva, Movimiento, db

T = TypeVar('T')


@dataclass
class ResultadoBuscar(Generic[T]):
    entidad: Optional[T] = None
    error: Tuple = ()


def _buscar_entidad(query, mensaje_error: str) -> ResultadoBuscar:
    resultado = ResultadoBuscar()
    entidad = db.session.execute(query).scalar_one_or_none()
    if not entidad:
        resultado.error = {'mensaje': mensaje_error}, 404
    resultado.entidad = entidad
    return resultado


def buscar_propiedad(id_propiedad: int, id_usuario: int) -> ResultadoBuscar[Propiedad]:
    query = select(Propiedad).filter(
        Propiedad.id == id_propiedad,
        (Propiedad.id_usuario == id_usuario) | (Propiedad.id_admin == id_usuario)
    )
    return _buscar_entidad(query, 'propiedad no encontrada')


def buscar_reserva(id_reserva: int, id_usuario: int) -> ResultadoBuscar[Reserva]:
    query = select(Reserva).join(Propiedad).filter(
        Reserva.id == id_reserva,
        (Propiedad.id_usuario == id_usuario) | (Propiedad.id_admin == id_usuario)
    )
    return _buscar_entidad(query, 'reserva no encontrada')


def buscar_movimiento(id_movimiento: int, id_usuario: int) -> ResultadoBuscar[Movimiento]:
    query = select(Movimiento).join(Propiedad).filter(
        Movimiento.id == id_movimiento,
        (Propiedad.id_usuario == id_usuario) | (Propiedad.id_admin == id_usuario)
    )
    return _buscar_entidad(query, 'movimiento no encontrado')
