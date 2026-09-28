
from flask import Flask
from flask import request
from os import environ
from model.model import Number, db
import os


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('SQLALCHEMY_DATABASE_URI') if environ.get('SQLALCHEMY_DATABASE_URI') != 'default' else 'sqlite:///conversion_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTION'] = True
    return app


app = create_app('default')
app_context = app.app_context()
app_context.push()
app.debug = True
db.init_app(app)
db.create_all()


@app.route('/guardar_numero',methods = ['POST'])
def SaveNumber():
    number = request.json["num_1"]
    new_number = Number(value=number)
    db.session.add(new_number)
    db.session.commit()
    return {"mensaje": f"numero {new_number.value} guardado correctamente."}


@app.route('/ultimo_numero',methods = ['GET'])
def GetNumber():
    last_record = db.session.query(Number).order_by(Number.id.desc()).first()
    return {"ultimo_valor": last_record.value}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)