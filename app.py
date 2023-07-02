'''
Este código importa diferentes módulos y clases necesarios para el desarrollo de una aplicación Flask.

Flask: Es la clase principal de Flask, que se utiliza para crear instancias de la aplicación Flask.
jsonify: Es una función que convierte los datos en formato JSON para ser enviados como respuesta desde la API.
request: Es un objeto que representa la solicitud HTTP realizada por el cliente.
CORS: Es una extensión de Flask que permite el acceso cruzado entre dominios (Cross-Origin Resource Sharing), lo cual es útil cuando se desarrollan aplicaciones web con frontend y backend separados.
SQLAlchemy: Es una biblioteca de Python que proporciona una abstracción de alto nivel para interactuar con bases de datos relacionales.
Marshmallow: Es una biblioteca de serialización/deserialización de objetos Python a/desde formatos como JSON.
Al importar estos módulos y clases, estamos preparando nuestro entorno de desarrollo para utilizar las funcionalidades que ofrecen.

'''
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow, fields, ValidationError

import enum

'''
En este código, se está creando una instancia de la clase Flask y se está configurando para permitir el acceso cruzado entre dominios utilizando el módulo CORS.

app = Flask(__name__): Se crea una instancia de la clase Flask y se asigna a la variable app. El parámetro __name__ es una variable que representa el nombre del módulo o paquete en el que se encuentra este código. Flask utiliza este parámetro para determinar la ubicación de los recursos de la aplicación.

CORS(app): Se utiliza el módulo CORS para habilitar el acceso cruzado entre dominios en la aplicación Flask. Esto significa que el backend permitirá solicitudes provenientes de dominios diferentes al dominio en el que se encuentra alojado el backend. Esto es útil cuando se desarrollan aplicaciones web con frontend y backend separados, ya que permite que el frontend acceda a los recursos del backend sin restricciones de seguridad del navegador. Al pasar app como argumento a CORS(), se configura CORS para aplicar las políticas de acceso cruzado a la aplicación Flask representada por app.

'''
# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

'''
En este código, se están configurando la base de datos y se están creando objetos para interactuar con ella utilizando SQLAlchemy y Marshmallow.

app.config["SQLALCHEMY_DATABASE_URI"]: Se configura la URI (Uniform Resource Identifier) de la base de datos. En este caso, se está utilizando MySQL como el motor de base de datos, el usuario y la contraseña son "root", y la base de datos se llama "proyecto". Esta configuración permite establecer la conexión con la base de datos.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: Se configura el seguimiento de modificaciones de SQLAlchemy. Al establecerlo en False, se desactiva el seguimiento automático de modificaciones en los objetos SQLAlchemy, lo cual mejora el rendimiento.

db = SQLAlchemy(app): Se crea un objeto db de la clase SQLAlchemy, que se utilizará para interactuar con la base de datos. Este objeto proporciona métodos y funcionalidades para realizar consultas y operaciones en la base de datos.

ma = Marshmallow(app): Se crea un objeto ma de la clase Marshmallow, que se utilizará para serializar y deserializar objetos Python a JSON y viceversa. Marshmallow proporciona una forma sencilla de definir esquemas de datos y validar la entrada y salida de datos en la aplicación. Este objeto se utilizará para definir los esquemas de los modelos de datos en la aplicación.

'''
# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/proyecto"
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = SQLAlchemy(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)


# CLASES DE SOPORTE (ENUM)

class FnEnum(enum.Enum): #Enumerador para los tres tipos de financiamiento de una clínica
    publico = 1
    privado = 2
    mixto = 3

class RtEnum(enum.Enum): #Enumerador para los tres tipos de rating
    instalaciones = 1
    medicos = 2
    servicio = 3

# TABLAS DE LA DB DEL PROYECTO

class Clinica(db.Model):  # Clase para tabla de Clínicas

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    financ = db.Column(db.Enum(FnEnum))
    direccion = db.Column(db.String(150))
    localidad = db.Column(db.String(50))
    imagen = db.Column(db.String(100))
    telefono = db.Column(db.String(10))
    # ratings establece la relación con la clase Rating (1-a-muchos)
    ratings = db.relationship("Rating", backref='clinica', cascade="all, delete-orphan", lazy=True)

    def __init__(self, nombre, financ, direccion, localidad, imagen, telefono):
        """
        Constructor de la clase Clinica.

        Args:
            nombre (str): Nombre de la clinica.
            financ (str): Tipo de clínica. Acepta dos valores: publico, privado o mixto.
            direccion (str): Domicilio de la clínica.
            localidad (str): Localidad de la clínica.
            telefono (str): Teléfono de la clínica.
            imagen (str): Nombre del archivo de imagen de la clínica
        """
        self.nombre = nombre
        self.financ = financ
        self.direccion = direccion
        self.localidad = localidad
        self.telefono = telefono
        self.imagen = imagen

class User(db.Model):  # Clase para tabla de Usuarios

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.db.String(20))
    pwd = db.Column(db.db.String(20))
    ratings = db.relationship("Rating", backref='user', cascade="all, delete-orphan", lazy=True)

    def __init__(self, handle, pwd):
        """
        Constructor de la clase User.

        Args:
            handle (str): Nombre de usuario
            pwd (str): Contraseña
        """
        self.handle = handle
        self.pwd = pwd


class Rating(db.Model):  # Clase para tabla de Ratings

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(RtEnum))
    valor = db.column(db.Integer, db.CheckConstraint('valor >= 1 AND valor <= 5'))
    id_clinica = db.Column(db.Integer, db.ForeignKey('clinica.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, tipo, valor, id_clinica, id_user):
        """
        Constructor de la clase Rating.

        Args:
            tipo (Enum): Registra el tipo de rating. Acepta tres valores: instalaciones, medicos, o servicio
            valor (int): Puntaje del tipo de rating. Utiliza constraints para limitar el valor entre 1 y 5 desde el DB management (redundancia)
            id_clinica (int): Clave foránea que vincula Rating con Clinica
            id_user (int): Clave foránea que vincula Rating con User
        """
        self.tipo = tipo
        self.valor = valor
        self.id_clinica = id_clinica
        self.id_user = id_user
    # Acá puedo agregar más clases para definir otras tablas en la base de datos


with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos


# DEFINICIONES DE SCHEMAS

class UserSchema(ma.Schema):
    """
    Esquema de la clase User.

    Este esquema define los campos que serán serializados/deserializados para la clase User.
    """
    class Meta:
        id = fields.Int(dump_only=True)
        handle = fields.Str(required=True)
        exclude = ("pwd")

class RatingSchema(ma.Schema):
    """
    Esquema de la clase Rating.

    Este esquema define los campos que serán serializados/deserializados para la clase Rating.
    """
    class Meta:
        id = fields.Int(dump_only=True)
        tipo = fields.Enum(Required=True)
        puntaje = fields.Str(Required=True)
        id_clinica = fields.Int(Required=True)
        id_user = fields.Int(Required=True)

class ClinicaSchema(ma.Schema):
    """
    Esquema de la clase Clinica.

    Este esquema define los campos que serán serializados/deserializados para la clase Clinica.
    """
    class Meta:
        id = fields.Int(dump_only=True)
        nombre = fields.Enum(Required=True)
        financ = fields.Str()
        direccion = fields.Int()
        localidad = fields.Int()
        telefono = fields.Str()
        imagen = fields.Str()
        ratings = fields.Nested(RatingSchema, many=True)

user_schema = UserSchema()  # Objeto para serializar/deserializar un usuario
users_schema = UserSchema(many=True)  # Objeto para serializar/deserializar múltiples usuarios

rating_schema = RatingSchema()  # Objeto para serializar/deserializar un rating
ratings_schema = RatingSchema(many=True)  # Objeto para serializar/deserializar múltiples ratings

clinica_schema = ClinicaSchema()  # Objeto para serializar/deserializar un rating
clinicas_schema = ClinicaSchema(many=True)  # Objeto para serializar/deserializar múltiples ratings


# ENDPOINDS DE LA DB DEL PROYECTO

#Endpoints para obtener listados de elementos
@app.route("/clinicas", methods=["GET"])
def get_Clinicas():
    """
    Endpoint para obtener todas las clínicas de la base de datos.

    Retorna un JSON con todos los registros de la tabla de clínicas, o con una página si se solicita un resultado paginado.
    """
    pag = request.args.get('pag', default=1, type=int)
    por_pag = request.args.get('por_pag', default=None, type=int)
    
    if por_pag is None:
        # Obtiene todos los registros de la tabla clínicas si no se definió un parámetro de resultados por página
        list_clinicas = Clinica.query.all() # Obtiene todos los registros de la tabla de clínicas
    else:
        # Calculate offset based on page and per_page
        offset = (pag - 1) * por_pag
        list_clinicas = Clinica.query.offset(offset).limit(por_pag).all()

    result = clinicas_schema.dump(list_clinicas)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/users", methods=["GET"])
def get_Users():
    """
    Endpoint para obtener todos los usuarios de la base de datos.

    Retorna un JSON con todos los registros de la tabla de usuarios, o con una página si se solicita un resultado paginado.
    """
    pag = request.args.get('pag', default=1, type=int)
    por_pag = request.args.get('por_pag', default=None, type=int)
    
    if por_pag is None:
        # Obtiene todos los registros de la tabla clínicas si no se definió un parámetro de resultados por página
        list_users = User.query.all() # Obtiene todos los registros de la tabla de clínicas
    else:
        # Calculate offset based on page and per_page
        offset = (pag - 1) * por_pag
        list_users = User.query.offset(offset).limit(por_pag).all()

    result = users_schema.dump(list_users)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/ratings", methods=["GET"])
def get_Ratings():
    """
    Endpoint para obtener todos los ratings de la base de datos.

    Retorna un JSON con todos los registros de la tabla de ratings, o con una página si se solicita un resultado paginado.
    """
    pag = request.args.get('pag', default=1, type=int)
    por_pag = request.args.get('por_pag', default=None, type=int)
    
    if por_pag is None:
        # Obtiene todos los registros de la tabla clínicas si no se definió un parámetro de resultados por página
        list_ratings = Rating.query.all() # Obtiene todos los registros de la tabla de clínicas
    else:
        # Calculate offset based on page and per_page
        offset = (pag - 1) * por_pag
        list_ratings = Rating.query.offset(offset).limit(por_pag).all()

    result = ratings_schema.dump(list_ratings)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

'''
Endpoints de las APIs de gestión:
get_#elemento#(id):
    # Obtiene un elemento específica de la tabla correspondiente
    # Retorna un JSON con la información del elemento correspondiente al ID proporcionado
delete_#elemento#(id):
    # Elimina un elemento de una tabla
    # Retorna un JSON con el registro eliminado del elemento correspondiente al ID proporcionado
create_#elemento#():
    # Crea un nuevo elemento en una tabla
    # Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro del tipo correspondiente
    # Retorna un JSON con la nueva clínica creada
update_#elemento#(id):
    # Actualiza un elemento existente en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del elemento con el ID especificado
    # Retorna un JSON con el elemento actualizad

'''

# Endpoints de CLÍNICAS:
@app.route("/clinicas/<id>", methods=["GET"])
def get_clinica(id):
    """
    Endpoint para obtener una clínica específica de la base de datos.

    Retorna un JSON con la información de la clínica correspondiente al ID proporcionado
    """
    clinica = Clinica.query.get(id)  # Obtiene la clínica correspondiente al ID recibido
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica

@app.route("/clinicas/<id>", methods=["DELETE"])
def delete_clinica(id):
    """
    Endpoint para eliminar una clinica de la base de datos.

    Elimina la clinica correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    clinica = Clinica.query.get(id)  # Obtiene la clinica correspondiente al ID recibido
    db.session.delete(clinica)  # Elimina la clinica de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON del producto eliminado

@app.route("/clinicas", methods=["POST"])  # Endpoint para crear una clinica
def create_clinica():
    """
    Endpoint para crear una nueva clinica en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de clinica en la base de datos.
    Retorna un JSON con la nuevo clinica creado.
    """
    json_data = request.get_json()

    if not json_data:
        return {"message": "No se ha provisto ningún dato para ingresar"}, 400
    
    
    data = clinica_schema.load(json_data)
    
    nombre = nombre
    financ = financ
    direccion = direccion
    localidad = localidad
    telefono = telefono
    imagen = imagen

    nombre = request.json["nombre"]        # Obtiene el nombre de la clínica del JSON proporcionado
    direccion = request.json["direccion"]  # Obtiene la dirección de la clínica del JSON proporcionado
    localidad = request.json["localidad"]  # Obtiene la localidad de la clínica del JSON proporcionado
    telefono = request.json["telefono"]    # Obtiene el teléfono de la clínica del JSON proporcionado
    imagen = request.json["imagen"]        # Obtiene la imagen de la clínica del JSON proporcionado
    rate_edil = request.json["rate_edil"]  # Obtiene el puntaje edilicio de la clínica del JSON proporcionado
    rate_medi = request.json["rate_medi"]  # Obtiene el puntaje médico de la clínica del JSON proporcionado
    rate_serv = request.json["rate_serv"]  # Obtiene el puntaje de servicios de la clínica del JSON proporcionado

    new_clinica = Clinica(nombre, direccion, localidad, imagen, telefono, rate_edil, rate_medi, rate_serv)  # Crea un nuevo objeto Clinica con los datos proporcionados
    db.session.add(new_clinica)  # Agrega la nueva clinica a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(new_clinica)  # Retorna el JSON de la nueva clínica creado

@app.route("/clinicas/<id>", methods=["PUT"])  # Endpoint para actualizar una clínica
def update_clinica(id):
    """
    Endpoint para actualizar una clínica existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro de la clínica con el ID especificado.
    Retorna un JSON con la clínica actualizada.
    """
    clinica = Clinica.query.get(id)  # Obtiene la clínica existente con el ID especificado

    # Actualiza los atributos de la clínica con los datos proporcionados en el JSON
    clinica.nombre = request.json["nombre"]
    clinica.direccion = request.json["direccion"]
    clinica.localidad = request.json["localidad"]
    clinica.telefono = request.json["telefono"]
    clinica.imagen = request.json["imagen"]
    clinica.rate_edil = request.json["rate_edil"]
    clinica.rate_medi = request.json["rate_medi"]
    clinica.rate_serv = request.json["rate_serv"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica actualizado

# Endpoints de CLÍNICAS:
@app.route("/clinicas/<id>", methods=["GET"])
def get_clinica(id):
    """
    Endpoint para obtener una clínica específica de la base de datos.

    Retorna un JSON con la información de la clínica correspondiente al ID proporcionado
    """
    clinica = Clinica.query.get(id)  # Obtiene la clínica correspondiente al ID recibido
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica

@app.route("/clinicas/<id>", methods=["DELETE"])
def delete_clinica(id):
    """
    Endpoint para eliminar una clinica de la base de datos.

    Elimina la clinica correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    clinica = Clinica.query.get(id)  # Obtiene la clinica correspondiente al ID recibido
    db.session.delete(clinica)  # Elimina la clinica de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON del producto eliminado

@app.route("/clinicas", methods=["POST"])  # Endpoint para crear una clinica
def create_clinica():
    """
    Endpoint para crear una nueva clinica en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de clinica en la base de datos.
    Retorna un JSON con la nuevo clinica creado.
    """
    nombre = request.json["nombre"]        # Obtiene el nombre de la clínica del JSON proporcionado
    direccion = request.json["direccion"]  # Obtiene la dirección de la clínica del JSON proporcionado
    localidad = request.json["localidad"]  # Obtiene la localidad de la clínica del JSON proporcionado
    telefono = request.json["telefono"]    # Obtiene el teléfono de la clínica del JSON proporcionado
    imagen = request.json["imagen"]        # Obtiene la imagen de la clínica del JSON proporcionado
    rate_edil = request.json["rate_edil"]  # Obtiene el puntaje edilicio de la clínica del JSON proporcionado
    rate_medi = request.json["rate_medi"]  # Obtiene el puntaje médico de la clínica del JSON proporcionado
    rate_serv = request.json["rate_serv"]  # Obtiene el puntaje de servicios de la clínica del JSON proporcionado

    new_clinica = Clinica(nombre, direccion, localidad, imagen, telefono, rate_edil, rate_medi, rate_serv)  # Crea un nuevo objeto Clinica con los datos proporcionados
    db.session.add(new_clinica)  # Agrega la nueva clinica a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(new_clinica)  # Retorna el JSON de la nueva clínica creado

@app.route("/clinicas/<id>", methods=["PUT"])  # Endpoint para actualizar una clínica
def update_clinica(id):
    """
    Endpoint para actualizar una clínica existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro de la clínica con el ID especificado.
    Retorna un JSON con la clínica actualizada.
    """
    clinica = Clinica.query.get(id)  # Obtiene la clínica existente con el ID especificado

    # Actualiza los atributos de la clínica con los datos proporcionados en el JSON
    clinica.nombre = request.json["nombre"]
    clinica.direccion = request.json["direccion"]
    clinica.localidad = request.json["localidad"]
    clinica.telefono = request.json["telefono"]
    clinica.imagen = request.json["imagen"]
    clinica.rate_edil = request.json["rate_edil"]
    clinica.rate_medi = request.json["rate_medi"]
    clinica.rate_serv = request.json["rate_serv"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica actualizado

# Endpoints de CLÍNICAS:
@app.route("/clinicas/<id>", methods=["GET"])
def get_clinica(id):
    """
    Endpoint para obtener una clínica específica de la base de datos.

    Retorna un JSON con la información de la clínica correspondiente al ID proporcionado
    """
    clinica = Clinica.query.get(id)  # Obtiene la clínica correspondiente al ID recibido
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica

@app.route("/clinicas/<id>", methods=["DELETE"])
def delete_clinica(id):
    """
    Endpoint para eliminar una clinica de la base de datos.

    Elimina la clinica correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    clinica = Clinica.query.get(id)  # Obtiene la clinica correspondiente al ID recibido
    db.session.delete(clinica)  # Elimina la clinica de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON del producto eliminado

@app.route("/clinicas", methods=["POST"])  # Endpoint para crear una clinica
def create_clinica():
    """
    Endpoint para crear una nueva clinica en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de clinica en la base de datos.
    Retorna un JSON con la nuevo clinica creado.
    """
    nombre = request.json["nombre"]        # Obtiene el nombre de la clínica del JSON proporcionado
    direccion = request.json["direccion"]  # Obtiene la dirección de la clínica del JSON proporcionado
    localidad = request.json["localidad"]  # Obtiene la localidad de la clínica del JSON proporcionado
    telefono = request.json["telefono"]    # Obtiene el teléfono de la clínica del JSON proporcionado
    imagen = request.json["imagen"]        # Obtiene la imagen de la clínica del JSON proporcionado
    rate_edil = request.json["rate_edil"]  # Obtiene el puntaje edilicio de la clínica del JSON proporcionado
    rate_medi = request.json["rate_medi"]  # Obtiene el puntaje médico de la clínica del JSON proporcionado
    rate_serv = request.json["rate_serv"]  # Obtiene el puntaje de servicios de la clínica del JSON proporcionado

    new_clinica = Clinica(nombre, direccion, localidad, imagen, telefono, rate_edil, rate_medi, rate_serv)  # Crea un nuevo objeto Clinica con los datos proporcionados
    db.session.add(new_clinica)  # Agrega la nueva clinica a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(new_clinica)  # Retorna el JSON de la nueva clínica creado

@app.route("/clinicas/<id>", methods=["PUT"])  # Endpoint para actualizar una clínica
def update_clinica(id):
    """
    Endpoint para actualizar una clínica existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro de la clínica con el ID especificado.
    Retorna un JSON con la clínica actualizada.
    """
    clinica = Clinica.query.get(id)  # Obtiene la clínica existente con el ID especificado

    # Actualiza los atributos de la clínica con los datos proporcionados en el JSON
    clinica.nombre = request.json["nombre"]
    clinica.direccion = request.json["direccion"]
    clinica.localidad = request.json["localidad"]
    clinica.telefono = request.json["telefono"]
    clinica.imagen = request.json["imagen"]
    clinica.rate_edil = request.json["rate_edil"]
    clinica.rate_medi = request.json["rate_medi"]
    clinica.rate_serv = request.json["rate_serv"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de producción
    app.run(debug=True, port=5000)