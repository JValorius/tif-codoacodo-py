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
# Importa las clases select y func del módulo sqlalchemy.sql, que serán necesarias para realizar queries avanzadas
from sqlalchemy.sql import select, func, text
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
# Importa la clase enum, para poder declarar enumeradores
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
    nombre = db.Column(db.String(150), nullable=False)
    financ = db.Column(db.Enum(FnEnum))
    direccion = db.Column(db.String(150))
    localidad = db.Column(db.String(50))
    website = db.Column(db.String(100))
    telefono = db.Column(db.String(10))
    imagen = db.Column(db.String(100))
    # ratings establece la relación con la clase Rating (1-a-muchos)
    ratings = db.relationship("Rating", backref='clinica', cascade="all, delete-orphan", lazy=True)

    def __init__(self, nombre, financ, direccion, localidad, website, telefono, imagen):
        """
        Constructor de la clase Clinica.

        Args:
            nombre (str): Nombre de la clinica.
            financ (str): Tipo de clínica. Acepta dos valores: publico, privado o mixto.
            direccion (str): Domicilio de la clínica.
            localidad (str): Localidad de la clínica.
            telefono (str): Teléfono de la clínica.
            website (str): Sitio web de la clínica.
            imagen (str): Nombre del archivo de imagen de la clínica
        """
        self.nombre = nombre
        self.financ = financ
        self.direccion = direccion
        self.localidad = localidad
        self.website = website
        self.telefono = telefono
        self.imagen = imagen
    '''
    Habilita la realización de la siguiente query:
    #  SELECT AVG(ratings.valor)
    #  FROM ratings
    #  WHERE ratings.id_clinica = <clinica> AND ratings.tipo = <tipo_rating>
    #  Devuelve un escalar igual al promedio de ratings del tipo <tipo_rating>
    '''
    '''
    @property
    def ratings_promedio(self):
        query = select([func.avg(Rating.valor)]).where(Rating.id_clinica == self.id).group_by(Rating.tipo)
        results = db.session.execute(query).fetchall()
        return results
    '''

class User(db.Model):  # Clase para tabla de Usuarios

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(20), unique= True, nullable=False)
    pwd = db.Column(db.String(20))
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

    # Acá puedo agregar más clases para definir otras tablas en la base de datos

class Rating(db.Model):  # Clase para tabla de Ratings

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(RtEnum), nullable=False)
    valor = db.column_property(db.Column(db.Integer, db.CheckConstraint('valor >= 1 AND valor <= 5'), nullable=False))
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

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos


# DEFINICIONES DE SCHEMAS

class UserSchema(ma.Schema):
    """
    Esquema de la clase User.

    Este esquema define los campos que serán serializados/deserializados para la clase User.
    """
    class Meta:
        fields = ("id", "handle")
        dump_only = ("id",)

class ClinicaSchema(ma.Schema):
    """
    Esquema de la clase Clinica.

    Este esquema define los campos que serán serializados/deserializados para la clase Clinica.
    """
    class Meta:
        fields = ("id", "nombre", "financ", "direccion", "localidad", "telefono", "website", "imagen", "promedio_inst", "promedio_medi", "promedio_serv")
        dump_only = ("id",)
        include_fk = False
    
   # avg_ratings = fields.Method("get_ratings_promedio")

    
    
class RatingSchema(ma.Schema):
    """
    Esquema de la clase Rating.

    Este esquema define los campos que serán serializados/deserializados para la clase Rating.
    """
    class Meta:
        dump_only = ("id","tipo","puntaje","id_clinica","nom_clinica","id_user", "nom_user")

    

UserSchema.ratings = fields.Nested(RatingSchema, many=True)
ClinicaSchema.ratings = fields.Nested(RatingSchema, many=True)

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
    
    # query = select([func.avg(Rating.valor)]).where(Rating.id_clinica == Clinica.id).group_by(Rating.tipo)
    query = text("""
            SELECT clinica.*,
            AVG(CASE WHEN rating.tipo = 'instalaciones' THEN CAST(rating.valor AS FLOAT) END) AS promedio_inst,
            AVG(CASE WHEN rating.tipo = 'medicos' THEN CAST(rating.valor AS FLOAT) END) AS promedio_medi,
            AVG(CASE WHEN rating.tipo = 'servicio' THEN CAST(rating.valor AS FLOAT) END) AS promedio_serv
            FROM clinica
            LEFT JOIN rating ON clinica.id = rating.id_clinica
            GROUP BY clinica.id;
            """)

    print(query)
    if por_pag is None:
        #  Obtiene todos los registros de la tabla clínicas si no se definió un parámetro de resultados por página
        list_clinicas = db.session.execute(query)
        print(list_clinicas)
    else:
        #  Si se definió un parámetro de resultados por página, pagina los resultados
        list_clinicas = db.paginate(query, pag, por_pag)

    result = clinicas_schema.dump(list_clinicas)  # Serializa los registros en formato JSON
    print(result)
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
        #  Obtiene todos los registros de la tabla usuarios si no se definió un parámetro de resultados por página
        list_users = db.session.execute(db.select(User))
    else:
        #  Si se definió un parámetro de resultados por página, pagina los resultados
        list_users = db.paginate(db.select(User), pag, por_pag)

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
        #  Obtiene todos los registros de la tabla usuarios si no se definió un parámetro de resultados por página
        list_ratings = db.session.execute(db.select(Rating))
    else:
        #  Si se definió un parámetro de resultados por página, pagina los resultados
        list_ratings = db.paginate(db.select(Rating), pag, por_pag)

    for rating in list_ratings:
        #  Busca el handle de usuario y el nombre de clínica para los ID correspondientes, y los agrega a los datos devueltos por el JSON
        id_user = rating['id_user']
        id_clinica = rating['id_clinica']
        user_handle = db.session.execute(db.select(User.c.handle).filter_by(id_user=id_user))
        nombre_clinica = db.session.execute(db.select(Clinica.c.nombre).filter_by(id_clinica=id_clinica))
        
        rating.user_handle = user_handle
        rating.nombre_clinica = nombre_clinica


    result = ratings_schema.dump(list_ratings)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

"""
Endpoints para cargar elementos en masa en la base de datos (por ejemplo, cargando un archivo JSON desde el FrontEnd)

Lee los datos proporcionados en formato JSON por el cliente y crea nuevos registros en la base de datos.
Retorna un JSON con la lista de registros actualizada.

Para esta función aplico métodos más concisos que en las funciones "create_<elemento>", que utilizan request.json para explicitar
los parámetros a recibir.
"""
@app.route("/clinicas", methods=["POST"])
def create_Clinicas():
    #  Recupera el JSON del request (si existe)
    json_data = request.get_json()

    #  Devuelve mensaje de advertencia en caso de no haber podido recuperar nada
    if not json_data:
        return {"message": "No se ha provisto ningún dato para ingresar"}, 400

    #  Crea un array de clínicas con los elementos del JSON
    clinicas = json_data.get('clinicas', [])

    for clinica in clinicas:
        #  Remueve el ID, si existe, para evitar conflictos
        clinica.pop(id, None) 

        nombre = clinica['nombre']
        direccion = direccion['direccion']
        '''
        Realiza la siguiente query:
        #  SELECT *
        #  FROM clinicas
        #  WHERE clinicas.nombre = '<nombre>' AND clinicas.direccion = '<direccion>'
        #  LIMIT 1
        #  Devuelve UN registro con las condiciones especificadas, si existe.
        '''
        clinica_duplicada = db.session.execute(db.select(Clinica).filter_by(nombre=nombre, direccion=direccion).first())
        #  Si existe el registro, saltear el paso de añadirlo a la carga de la DB
        if clinica_duplicada:
            continue

        new_clinica = Clinica(**clinica)
        db.session.add(new_clinica)
    
    db.session.add_all(clinicas)  # Agrega la lista de clinicas a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinicas_schema.jsonify(clinicas)  # Retorna el JSON de la lista de clínicas actualizada

@app.route("/ratings", methods=["POST"])
def create_Ratings():
    #  Recupera el JSON del request (si existe)
    json_data = request.get_json()

    #  Devuelve mensaje de advertencia en caso de no haber podido recuperar nada
    if not json_data:
        return {"message": "No se ha provisto ningún dato para ingresar"}, 400

    #  Crea un array de ratings con los elementos del JSON
    ratings = json_data.get('ratings', [])

    for rating in ratings:
        #  Remueve el ID, si existe, para evitar conflictos
        rating.pop(id, None)
        
        id_user = rating['id_user']
        id_clinica = rating['id_clinica']
        tipo = rating['tipo']
        '''
        Realiza la siguiente query:
        #  SELECT *
        #  FROM ratings
        #  WHERE ratings.tipo = '<tipo>' AND ratings.id_user = '<id_user>' AND id_clinica = '<id_clinica>'
        #  LIMIT 1
        #  Devuelve UN registro con las condiciones especificadas, si existe.
        '''
        rating_duplicado = db.session.execute(db.select(Rating).filter_by(tipo=tipo, id_user=id_user, id_clinica=id_clinica).first())
        #  Si existe el registro, saltear el paso de añadirlo a la carga de la DB, salvo que el ID de usuario sea 1,
        #  porque podemos usarlo para carga masiva sin afectar usuarios reales. 
        if rating_duplicado and id_user != 1:
            continue

        new_rating = Rating(**rating)
        db.session.add(new_rating)
    
    db.session.add_all(ratings)  # Agrega la lista de ratings a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return ratings_schema.jsonify(ratings)  # Retorna el JSON de la lista de ratings actualizada


'''
Otros Endpoints de las APIs de gestión:
get_<elemento>(id):
    # Obtiene un elemento específica de la tabla correspondiente
    # Retorna un JSON con la información del elemento correspondiente al ID proporcionado
delete_<elemento>(id):
    # Elimina un elemento de una tabla
    # Retorna un JSON con el registro eliminado del elemento correspondiente al ID proporcionado
create_<elemento>():
    # Crea un nuevo elemento en una tabla
    # Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro del tipo correspondiente
    # Retorna un JSON con la nueva clínica creada
update_<elemento>(id):
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
    clinica = db.get_or_404(Clinica, id, "No se encontró el ID indicado")  # Obtiene la clínica correspondiente al ID recibido
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica

@app.route("/clinicas/<id>", methods=["DELETE"])
def delete_clinica(id):
    """
    Endpoint para eliminar una clinica de la base de datos.

    Elimina la clinica correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    clinica = db.get_or_404(Clinica, id, "No se encontró el ID indicado")  # Obtiene la clinica correspondiente al ID recibido
    db.session.delete(clinica)  # Elimina la clinica de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica eliminada

@app.route("/clinicas", methods=["POST"])  # Endpoint para crear una clinica
def create_clinica():
    """
    Endpoint para crear una nueva clinica en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de clinica en la base de datos.
    Retorna un JSON con la nueva clinica creada.
    """

    nombre = request.json["nombre"]        # Obtiene el nombre de la clínica del JSON proporcionado
    financ = request.json["financ"]        # Obtiene el tipo de la clínica del JSON proporcionado
    direccion = request.json["direccion"]  # Obtiene la dirección de la clínica del JSON proporcionado
    localidad = request.json["direccion"]  # Obtiene la dirección de la clínica del JSON proporcionado
    telefono = request.json["telefono"]    # Obtiene el teléfono de la clínica del JSON proporcionado
    website = request.json["website"]      # Obtiene el sitio web de la clínica del JSON proporcionado
    imagen = request.json["imagen"]        # Obtiene la imagen de la clínica del JSON proporcionado

    new_clinica = Clinica(nombre, financ, direccion, localidad, telefono, website, imagen)  # Crea un objeto Clinica con los datos proporcionados
    db.session.add(new_clinica)  # Agrega la nueva clinica a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(new_clinica)  # Retorna el JSON de la nueva clínica creada

@app.route("/clinicas/<id>", methods=["PUT"])  # Endpoint para actualizar una clínica
def update_clinica(id):
    """
    Endpoint para actualizar una clínica existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro de la clínica con el ID especificado.
    Retorna un JSON con la clínica actualizada.
    """
    clinica = db.get_or_404(Clinica, id, "No se encontró el ID indicado")  # Obtiene la clínica existente con el ID especificado

    # Actualiza los atributos de la clínica con los datos proporcionados en el JSON
    clinica.nombre = request.json["nombre"]
    clinica.financ = request.json["financ"]
    clinica.direccion = request.json["direccion"]
    clinica.localidad = request.json["localidad"]
    clinica.website = request.json["website"]
    clinica.telefono = request.json["telefono"]
    clinica.imagen = request.json["imagen"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica actualizada


# Endpoints de RATINGS:
@app.route("/ratings/<id>", methods=["GET"])
def get_rating(id):
    """
    Endpoint para obtener un rating específico de la base de datos.

    Retorna un JSON con la información del rating correspondiente al ID proporcionado
    """
    rating = db.get_or_404(Rating, id, "No se encontró el ID indicado")  # Obtiene el rating correspondiente al ID recibido
    #  Busca el handle de usuario y el nombre de clínica para los ID correspondientes, y los agrega a los datos devueltos por el JSON
    id_user = rating['id_user']
    id_clinica = rating['id_clinica']
    user_handle = db.session.execute(db.select(User.c.handle).filter_by(id_user=id_user))
    nombre_clinica = db.session.execute(db.select(Clinica.c.nombre).filter_by(id_clinica=id_clinica))
        
    rating.user_handle = user_handle
    rating.nombre_clinica = nombre_clinica

    return rating_schema.jsonify(rating)  # Retorna el JSON del rating

@app.route("/ratings/<id>", methods=["DELETE"])
def delete_rating(id):
    """
    Endpoint para eliminar un rating de la base de datos.

    Elimina el rating correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    rating = db.get_or_404(Rating, id, "No se encontró el ID indicado")  # Obtiene el rating correspondiente al ID recibido
    db.session.delete(rating)  # Elimina el rating de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return rating_schema.jsonify(rating)  # Retorna el JSON del rating eliminado

@app.route("/ratings", methods=["POST"])  # Endpoint para crear una clinica
def create_rating():
    """
    Endpoint para crear un nuevo rating en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de rating en la base de datos.
    Retorna un JSON con la nuevo rating creado.
    """
    tipo = request.json["tipo"]             # Obtiene el tipo del rating del JSON proporcionado
    valor = request.json["valor"]           # Obtiene el valor del rating del JSON proporcionado
    id_user = request.json["id_user"]       # Obtiene el ID de usuario del rating del JSON proporcionado
    id_clinica = request.json["id_clinica"] # Obtiene el ID de clínica del rating del JSON proporcionado

    new_rating = Rating(tipo, valor, id_user, id_clinica)  # Crea un nuevo objeto Rating con los datos proporcionados
    db.session.add(new_rating)  # Agrega el nuevo rating a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return rating_schema.jsonify(new_rating)  # Retorna el JSON del nuevo rating creado

@app.route("/ratings/<id>", methods=["PUT"])  # Endpoint para actualizar un rating
def update_rating(id):
    """
    Endpoint para actualizar un rating existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del rating con el ID especificado.
    Retorna un JSON con el rating actualizado.
    """
    rating = db.get_or_404(Rating, id, "No se encontró el ID indicado")  # Obtiene el rating existente con el ID especificado

    # Actualiza los atributos del rating con los datos proporcionados en el JSON
    rating.tipo = request.json["tipo"]
    rating.valor = request.json["valor"]
    rating.id_user = request.json["id_user"]
    rating.id_clinica = request.json["id_clinica"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return rating_schema.jsonify(rating)  # Retorna el JSON del rating actualizado


# Endpoints de USUARIOS:
@app.route("/users/<id>", methods=["GET"])
def get_users(id):
    """
    Endpoint para obtener un usuario específico de la base de datos.

    Retorna un JSON con la información del usuario correspondiente al ID proporcionado
    """
    user = db.get_or_404(User, id, "No se encontró el ID indicado")  # Obtiene el usuario correspondiente al ID recibido
    return user_schema.jsonify(user)  # Retorna el JSON del usuario

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    """
    Endpoint para eliminar un usuario de la base de datos.

    Elimina el usuario correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    user = db.get_or_404(User, id, "No se encontró el ID indicado")   # Obtiene el usuario correspondiente al ID recibido
    db.session.delete(user)  # Elimina el usuario de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return user_schema.jsonify(user)  # Retorna el JSON del usuario eliminado

@app.route("/users", methods=["POST"])  # Endpoint para crear una clinica
def create_user():
    """
    Endpoint para crear un nuevo usuario en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de usuario en la base de datos.
    Retorna un JSON con la nuevo rating creado.
    """
    handle = request.json["handle"] # Obtiene el nombre del usuario del JSON proporcionado


    new_user = User(handle)  # Crea un nuevo objeto User con los datos proporcionados
    db.session.add(new_user)  # Agrega el nuevo usuario a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return user_schema.jsonify(new_user)  # Retorna el JSON del nuevo usuario creado

@app.route("/users/<id>", methods=["PUT"])  # Endpoint para actualizar un usuario
def update_user(id):
    """
    Endpoint para actualizar un usuario existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del usuario con el ID especificado.
    Retorna un JSON con el usuario actualizado.
    """
    user = db.get_or_404(User, id, "No se encontró el ID indicado")   # Obtiene el usuario existente con el ID especificado

    # Actualiza los atributos del usuario con los datos proporcionados en el JSON
    user.handle = request.json["handle"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return user_schema.jsonify(user)  # Retorna el JSON del usuario actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de producción
    app.run(debug=True, port=5000)