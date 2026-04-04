# 3rd Party Libraries
from flask import request
from sqlalchemy import select
from flask_restful import Resource
from flask_jwt_extended import current_user, jwt_required
from modelos import CategoriaMovimiento, CategoriaMovimientoSchema, db

# Instanciar categoria esquema
categoria_schema = CategoriaMovimientoSchema()

# Instanciar categorias esquema
categorias_schema = CategoriaMovimientoSchema(many = True)

class VistasCategorias(Resource):
    
    @jwt_required()
    def get(self):
        """Metodo que devuelve todas las categorias de movimientos de un usuario."""
        
        # Filtramos las categorias del usuario actual y las ordenamos por nombre
        categorias = db.session.execute(select(CategoriaMovimiento).filter(CategoriaMovimiento.id_usuario == current_user.id).order_by(CategoriaMovimiento.nombre.asc())).scalars().all()
        
        # Retorno de la lista de categorias
        return categorias_schema.dump(categorias)
    
    @jwt_required()
    def post(self):
        """Metodo que crea una nueva categoria de movimiento para un usuario."""

        # Obtener el nombre de la categoria del JSON
        nombre = request.json.get("nombre").strip()

        # Validar que el nombre no sea vacio
        if not nombre:
            return {"mensaje": "El nombre de la categoria es requerido"}, 400
        
        # Validar que el nombre no contenga caracteres especiales
        if not nombre.replace(" ", "").isalnum():
            return {"mensaje": "El nombre de la categoria no puede contener caracteres especiales"}, 400
        
        # Validar que el nombre no sea duplicado
        duplicado = db.session.execute(select(CategoriaMovimiento).filter(CategoriaMovimiento.id_usuario == current_user.id, CategoriaMovimiento.nombre == nombre)).scalar_one_or_none()

        # Validar que el nombre no sea duplicado
        if duplicado:
            return {"mensaje": f"Ya existe una categoria con el nombre: {nombre}"}, 409
        
        # Crear la nueva categoria
        nueva_categoria = CategoriaMovimiento(nombre = nombre, id_usuario = current_user.id)
        
        # Guardar la nueva categoria en la base de datos
        db.session.add(nueva_categoria)
        db.session.commit()

        return categoria_schema.dump(nueva_categoria), 201