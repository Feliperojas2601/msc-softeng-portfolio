# 3rd Party Libraries
from flask import request
from sqlalchemy import select
from flask_restful import Resource
from flask_jwt_extended import current_user, jwt_required
from modelos import CategoriaMovimiento, CategoriaMovimientoSchema, Movimiento, db

# Instanciar categoria esquema
categoria_schema = CategoriaMovimientoSchema()

class VistaCategoria(Resource):

    @jwt_required()
    def get(self, id_categoria):
        """Metodo que devuelve una categoria de movimiento de un usuario."""
        
        # Filtramos las categorias del usuario actual y las ordenamos por nombre
        categoria = db.session.execute(select(CategoriaMovimiento).filter(CategoriaMovimiento.id_usuario == current_user.id, CategoriaMovimiento.id == id_categoria)).scalar_one_or_none()
        
        # Retorno de la lista de categorias
        if not categoria:
            return {"mensaje": "Categoria no encontrada"}, 404
        
        # Retorno de la lista de categorias
        return categoria_schema.dump(categoria)

    @jwt_required()
    def put(self, id_categoria):
        """Metodo que actualiza una categoria de movimiento de un usuario."""
        
        # Filtramos las categorias del usuario actual y las ordenamos por nombre
        categoria = db.session.execute(select(CategoriaMovimiento).filter(CategoriaMovimiento.id_usuario == current_user.id, CategoriaMovimiento.id == id_categoria)).scalar_one_or_none()
        
        # Retorno de la lista de categorias
        if not categoria:
            return {"mensaje": "Categoria no encontrada"}, 404
        
        # Obtener el nombre de la categoria del JSON
        nombre = request.json.get("nombre").strip()

        # Validar que el nombre no sea vacio
        if not nombre:
            return {"mensaje": "El nombre de la categoria es requerido"}, 400
        
        # ↓ Agregar esta validación que falta
        if not nombre.replace(' ', '').isalnum():
            return {"mensaje": "El nombre no puede contener caracteres especiales"}, 400
        
        # Validar que el nombre no se encuentre duplicado
        duplicado = db.session.execute(select(CategoriaMovimiento).filter(CategoriaMovimiento.id_usuario == current_user.id, CategoriaMovimiento.nombre == nombre, CategoriaMovimiento.id != id_categoria)).scalar_one_or_none()

        # Mensaje de error en caso de duplicado
        if duplicado:
            return {"mensaje": f"Ya existe una categoria con el nombre {nombre}"}, 409
        
        # Actualizar la categoria
        categoria.nombre = nombre
        db.session.commit()

        # Retorno de la lista de categorias
        return categoria_schema.dump(categoria)
    
    @jwt_required()
    def delete(self, id_categoria):
        """Metodo que elimina una categoria de movimiento de un usuario."""

        # Filtramos las categorias del usuario actual y las ordenamos por nombre
        categoria = db.session.execute(select(CategoriaMovimiento).filter(CategoriaMovimiento.id_usuario == current_user.id, CategoriaMovimiento.id == id_categoria)).scalar_one_or_none()

        # Retorno de la lista de categorias
        if not categoria:
            return {"mensaje": "Categoria no encontrada"}, 404
        
        # Conservar el nombre de la categoria para el mensaje de retorno
        nombre = categoria.nombre
        
        # Verificar que la categoria no tenga movimientos
        en_movimientos = db.session.execute(select(Movimiento).filter(Movimiento.id_categoria == id_categoria)).scalar_one_or_none()

        # Retorno de la lista de categorias
        if en_movimientos:
            return {"mensaje": f"La categoría: {nombre}, esta asociada al movimiento: {en_movimientos.concepto}, y no puede ser eliminada"}, 400
        
        # Eliminar la categoria
        db.session.delete(categoria)
        db.session.commit()

        # Retorno de la lista de categorias
        return {"mensaje": f"Categoria '{nombre}' eliminada exitosamente"}, 204
        