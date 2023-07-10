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
import typing as t
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request, abort
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa las clases Pagination y SelectPagination del módulo flask_sqlalchemy. Utilizado para crear children de SQLAlchemy y SelectPagination
from flask_sqlalchemy.pagination import Pagination, SelectPagination
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
app.config ['JSON_SORT_KEYS'] = False
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

'''
En este código, se están configurando la base de datos y se están creando objetos para interactuar con ella utilizando SQLAlchemy y Marshmallow.

app.config["SQLALCHEMY_DATABASE_URI"]: Se configura la URI (Uniform Resource Identifier) de la base de datos. En este caso, se está utilizando MySQL como el motor de base de datos, el usuario y la contraseña son "root", y la base de datos se llama "proyecto". Esta configuración permite establecer la conexión con la base de datos.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: Se configura el seguimiento de modificaciones de SQLAlchemy. Al establecerlo en False, se desactiva el seguimiento automático de modificaciones en los objetos SQLAlchemy, lo cual mejora el rendimiento.

db = SQLAlchemy(app): Se crea un objeto db de la clase SQLAlchemy, que se utilizará para interactuar con la base de datos. Este objeto proporciona métodos y funcionalidades para realizar consultas y operaciones en la base de datos.

ma = Marshmallow(app): Se crea un objeto ma de la clase Marshmallow, que se utilizará para serializar y deserializar objetos Python a JSON y viceversa. Marshmallow proporciona una forma sencilla de definir esquemas de datos y validar la entrada y salida de datos en la aplicación. Este objeto se utilizará para definir los esquemas de los modelos de datos en la aplicación.
'''

#=========================================================================================================================================
# FUNCIONES Y CLASES PERSONALIZADAS
#=========================================================================================================================================
# Clase AltSelect, opera como SelectPagination, con la excepción que devuelve una query en forma de tuplas en lugar de escalares (necesario debido a que scalars() no opera bien sobre compound selects (como la query que realizamos en get_Clinicas_Rated))
class AltSelect(SelectPagination):
    def _query_items(self) -> list[t.Any]:
        select = self._query_args["select"]
        select = select.limit(self.per_page).offset(self._query_offset)
        session = self._query_args["session"]
        return list(session.execute(select))
    
    def _query_count(self) -> int:
        select = self._query_args["select"]
        sub = select.options(sa_orm.lazyload("*")).order_by(None).subquery()
        session = self._query_args["session"]
        out = session.execute(sa.select(sa.func.count()).select_from(sub))
        return out  # type: ignore[no-any-return]

# Clase AltSQLAlch, añade el método paginate_tuples, que funciona de igual forma que paginate, excepto que implementa AltSelect en lugar de SelectPagination. Nuestra forma de acceder a la paginación alternativa.
class AltSQLAlch (SQLAlchemy):
    def paginate_tuples(
        self,
        select: sa.sql.Select[t.Any],
        *,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = None,
        error_out: bool = True,
        count: bool = True,
    ) -> Pagination:
        return AltSelect(
            select=select,
            session=self.session(),
            page=page,
            per_page=per_page,
            max_per_page=max_per_page,
            error_out=error_out,
            count=count,
        )


# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://Usuario:password@UrlBD/nombreBD
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://JValorius:CLAVEACA@JValorius.mysql.pythonanywhere-services.com/JValorius$proyecto"
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = AltSQLAlch(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)

#=========================================================================================================================================
# CLASES DE SOPORTE (ENUM)
#=========================================================================================================================================
class FnEnum(str, enum.Enum): #Enumerador para los tres tipos de financiamiento de una clínica
    publico: str = "publico"
    privado: str = "privado"
    mixto: str = "mixto"

#=========================================================================================================================================
# TABLAS DE LA DB DEL PROYECTO
#=========================================================================================================================================
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

class Usuario(db.Model):  # Clase para tabla de Usuarios

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(20), unique= True, nullable=False)
    pwd = db.Column(db.String(20))
    ratings = db.relationship("Rating", backref='usuario', cascade="all, delete-orphan", lazy=True)

    def __init__(self, handle, pwd):
        """
        Constructor de la clase Usuario.

        Args:
            handle (str): Nombre de usuario
            pwd (str): Contraseña
        """
        self.handle = handle
        self.pwd = pwd

    # Acá puedo agregar más clases para definir otras tablas en la base de datos

class Rating(db.Model):  # Clase para tabla de Ratings

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    valor = db.column_property(db.Column(db.Integer, db.CheckConstraint('valor >= 1 AND valor <= 5'), nullable=False))
    id_clinica = db.Column(db.Integer, db.ForeignKey('clinica.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __init__(self, tipo, valor, id_clinica, id_user):
        """
        Constructor de la clase Rating.

        Args:
            tipo (str): Registra el tipo de rating. Acepta tres valores: instalaciones, medicos, o servicio
            valor (int): Puntaje del tipo de rating. Utiliza constraints para limitar el valor entre 1 y 5 desde el DB management (redundancia)
            id_clinica (int): Clave foránea que vincula Rating con Clinica
            id_user (int): Clave foránea que vincula Rating con Usuario
        """
        self.tipo = tipo
        self.valor = valor
        self.id_clinica = id_clinica
        self.id_user = id_user

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

#=========================================================================================================================================
# DEFINICIONES DE SCHEMAS
#=========================================================================================================================================
class UsuarioSchema(ma.Schema):
    """
    Esquema de la clase Usuario.

    Este esquema define los campos que serán serializados/deserializados para la clase Usuario.
    """
    class Meta:
        ordered = True
        fields = ("id", "handle")
        dump_only = ("id",)
        include_fk = False # Ignorar las foreign keys en esta versión de la app

usuario_schema = UsuarioSchema()  # Objeto para serializar/deserializar un usuario
usuarios_schema = UsuarioSchema(many=True)  # Objeto para serializar/deserializar múltiples usuarios
        
class ClinicaSchema(ma.Schema):
    """
    Esquema de la clase Clinica, construido para calcular ratings promedio desde el schema.

    Este esquema define los campos que serán serializados/deserializados para la clase Clinica, con ratings promedio anexados.
    """
    class Meta:
        ordered = True
        fields = ("id", "nombre", "financ", "direccion", "localidad", "telefono", "website", "imagen", "avg_ratings")
        dump_only = ("id",)
    
    avg_ratings = fields.Method("get_ratings_promedio")

    # Método para calcular los ratogs promedio. Itera sobre los objetos anidados, permitiendo agregarlos en un campo independiente.
    def get_ratings_promedio(self, clinica):
        if clinica.ratings:
            insta = []
            medic = []
            servi = []
            for rating in clinica.ratings:
                if rating.tipo == "instalaciones":
                    insta.append(rating.valor)
                if rating.tipo == "medicos":
                    medic.append(rating.valor)
                if rating.tipo == "servicio":
                    servi.append(rating.valor)
            prom_inst = sum(insta) / len(insta)
            prom_medi = sum(medic) / len(medic)
            prom_serv = sum(servi) / len(servi)
            return {"promedio_inst": prom_inst, "promedio_medi": prom_medi, "promedio_serv": prom_serv}
        return 0

clinica_schema = ClinicaSchema()  # Objeto para serializar/deserializar una clinica
clinicas_schema = ClinicaSchema(many=True)  # Objeto para serializar/deserializar múltiples ratings

class ClinicaAltSchema(ma.Schema):
    """
    Esquema de la clase Clinica, construido para tomar valores de ratings promedio de una query en endpoint.

    Este esquema define los campos que serán serializados/deserializados para la clase Clinica, con ratings promedio anexados.
    """
    class Meta:
        fields = ("id", "nombre", "financ", "direccion", "localidad", "telefono", "website", "imagen", "promedio_inst", "promedio_medi", "promedio_serv")
        dump_only = ("id",)

clinica_rating_schema = ClinicaAltSchema()  # Objeto para serializar/deserializar un rating
clinicas_rating_schema = ClinicaAltSchema(many=True)  # Objeto para serializar/deserializar múltiples ratings

class RatingSchema(ma.Schema):
    """
    Esquema de la clase Rating.

    Este esquema define los campos que serán serializados/deserializados para la clase Rating.
    """
    class Meta:
        ordered = True
        fields = ("id","tipo","valor","id_clinica","id_user", "clinica", "usuario")
        dump_only = ("id","id_clinica","id_user", "clinica", "usuario")
    
    clinica = ma.Nested(ClinicaSchema)
    usuario = ma.Nested(UsuarioSchema)

rating_schema = RatingSchema()  # Objeto para serializar/deserializar un rating
ratings_schema = RatingSchema(many=True)  # Objeto para serializar/deserializar múltiples ratings

#=========================================================================================================================================
# ENDPOINDS DE LA DB DEL PROYECTO
#=========================================================================================================================================
#Endpoints para obtener listados de elementos
@app.route("/clinicas_rated", methods=["GET"])
def get_Clinicas_Rated():
    """
    Endpoint para obtener todas las clínicas de la base de datos, con sus promedios de ratings a través de una única query. Más eficiente que calcularlos desde el schema. LEGACY: Conservada para futuras referencias

    Retorna un JSON paginado de registros de la tabla clínicas.
    """
    pagina = request.args.get('page', default=None, type=int)

    """Ejecutar la siguiente query:
    SELECT clinica.*,
    AVG(CASE WHEN rating.tipo = 'instalaciones' THEN CAST(rating.valor AS FLOAT) END) AS promedio_inst,
    AVG(CASE WHEN rating.tipo = 'medicos' THEN CAST(rating.valor AS FLOAT) END) AS promedio_medi,
    AVG(CASE WHEN rating.tipo = 'servicio' THEN CAST(rating.valor AS FLOAT) END) AS promedio_serv
    FROM clinica
    LEFT JOIN rating ON clinica.id = rating.id_clinica
    GROUP BY clinica.id;
    """
    prom_inst = db.func.avg(db.case((Rating.tipo == 'instalaciones', db.cast(Rating.valor, db.Float)))).label('promedio_inst')
    prom_medi = db.func.avg(db.case((Rating.tipo == 'medicos', db.cast(Rating.valor, db.Float)))).label('promedio_medi')
    prom_serv = db.func.avg(db.case((Rating.tipo == 'servicio', db.cast(Rating.valor, db.Float)))).label('promedio_serv')
    cl_query = db.select(Clinica, prom_inst, prom_medi, prom_serv).select_from(Clinica).outerjoin(Rating, Clinica.id == Rating.id_clinica).group_by(Clinica.id)

    list_clinicas = db.paginate_tuples(cl_query)
    
    formatted_result = []
    for item in list_clinicas:
        # Extraer los atributos deseados
        clinica_data = {
            'id': item[0].id,
            'nombre': item[0].nombre,
            'financ': item[0].financ,
            'direccion': item[0].direccion,
            'localidad': item[0].localidad,
            'website': item[0].website,
            'telefono': item[0].telefono,
            'imagen': item[0].imagen,
            # Extraer el resto de los atributos de las tuplas
            'promedio_inst': item[1],
            'promedio_medi': item[2],
            'promedio_serv': item[3]
        }

        formatted_result.append(clinica_data)

    result = clinicas_rating_schema.dump(formatted_result)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/clinicas", methods=["GET"])
def get_Clinicas():
    """
    Endpoint para obtener todas las clínicas de la base de datos.

    Retorna un JSON con un resultado paginado de registros, o con la tabla completa si se establece el parámetro pagina como 0
    """
    # pagina = request.args.get('page', default=None, type=int)
    
    # if pagina == 0:
        #  Obtiene todos los registros de la tabla clinicas si el parámetro page es igual a 0
    list_clinicas = db.session.execute(db.select(Clinica).order_by(Clinica.nombre)).scalars()
    # else:
        #  Si se definió un parámetro de resultados por página, pagina los resultados
        # list_clinicas = db.paginate(db.select(Clinica))
    result = clinicas_schema.dump(list_clinicas)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/usuarios", methods=["GET"])
def get_Usuarios():
    """
    Endpoint para obtener todos los usuarios de la base de datos.

    Retorna un JSON con un resultado paginado de registros, o con la tabla completa si se establece el parámetro pagina como 0
    """
    # pagina = request.args.get('page', default=None, type=int)
    
    #if pagina == 0:
        #  Obtiene todos los registros de la tabla usuarios si el parámetro page es igual a 0
    list_usuarios = db.session.execute(db.select(Usuario)).scalars()
    #else:
        #  Si se definió un parámetro de resultados por página, pagina los resultados
    #    list_usuarios = db.paginate(db.select(Usuario))

    result = usuarios_schema.dump(list_usuarios)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/ratings", methods=["GET"])
def get_Ratings():
    """
    Endpoint para obtener todos los ratings de la base de datos.

    Retorna un JSON con un resultado paginado de registros, o con la tabla completa si se establece el parámetro pagina como 0
    """
    # pagina = request.args.get('page', default=None, type=int)

    # if pagina == 0:
        #  Obtiene todos los registros de la tabla clinicas si el parámetro page es igual a 0
    list_ratings = db.session.execute(db.select(Rating).order_by(Rating.id_clinica, Rating.tipo)).scalars()
    #else:
        #  Si se definió un parámetro de resultados por página, pagina los resultados
    #    list_ratings = db.paginate(db.select(Rating))

    result = ratings_schema.dump(list_ratings)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

#=========================================================================================================================================
"""
Endpoints para cargar elementos en masa en la base de datos (por ejemplo, cargando un archivo JSON desde el FrontEnd)

Lee los datos proporcionados en formato JSON por el cliente y crea nuevos registros en la base de datos.
Retorna un JSON con la lista de registros actualizada.

Para esta función aplico métodos más concisos que en las funciones "create_<elemento>", que utilizan request.json para explicitar
los parámetros a recibir.
"""
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
        
        nw_id_user = rating['id_user']
        nw_id_clinica = rating['id_clinica']
        nw_tipo = rating['tipo']
        '''
        Realiza la siguiente query:
        #  SELECT *
        #  FROM ratings
        #  WHERE ratings.tipo = '<tipo>' AND ratings.id_user = '<id_user>' AND id_clinica = '<id_clinica>'
        #  LIMIT 1
        #  Devuelve UN registro con las condiciones especificadas, si existe.
        '''
        rating_duplicado = db.session.execute(db.select(Rating).filter_by(tipo=nw_tipo, id_user=nw_id_user, id_clinica=nw_id_clinica).first())
        #  Si existe el registro, saltear el paso de añadirlo a la carga de la DB, salvo que el ID de usuario sea 1,
        #  porque podemos usarlo para carga masiva sin afectar usuarios reales. 
        if rating_duplicado and nw_id_user != 1:
            continue

        new_rating = Rating(**rating)
        db.session.add(new_rating)
    
    db.session.add_all(ratings)  # Agrega la lista de ratings a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return ratings_schema.jsonify(ratings)  # Retorna el JSON de la lista de ratings actualizada
"""

#=========================================================================================================================================
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
#=========================================================================================================================================
# Endpoints de CLÍNICAS:
@app.route("/clinicas/<id>", methods=["GET"])
def get_clinica(id):
    """
    Endpoint para obtener una clínica específica de la base de datos.

    Retorna un JSON con la información de la clínica correspondiente al ID proporcionado
    """
    """
    Endpoint para obtener todas las clínicas de la base de datos.

    Retorna un JSON con todos los registros de la tabla de clínicas, o con una página si se solicita un resultado paginado.
    """
    clinica = db.get_or_404(Clinica, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.") # Obtiene la clínica correspondiente al ID recibido. Devuelve mensaje personalizado 404 si no se encuentra.
    return clinica_schema.jsonify(clinica)  # Retorna el JSON de la clínica

@app.route("/clinicas/<id>", methods=["DELETE"])
def delete_clinica(id):
    """
    Endpoint para eliminar una clinica de la base de datos.

    Elimina la clinica correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    clinica = db.get_or_404(Clinica, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.") # Obtiene la clinica correspondiente al ID recibido
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
    clinica = db.get_or_404(Clinica, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.")  # Obtiene la clínica existente con el ID especificado

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

@app.route("/clinicas/filter", methods=["GET"])  # Endpoint para filtrar clínicas por nombre
def filtrar_clinica():
    # extrae el término de búsqueda de los argumentos de la query
    texto = request.args.get('term', default=None, type=str)

    filt_query = db.select(Clinica).filter(Clinica.nombre.ilike(f'%{texto}%'))
    filtro_clinicas = db.session.execute(filt_query).scalars()
    result = clinicas_schema.dump(filtro_clinicas)
    if result:
        return jsonify(result)
    else:
        abort(404, description="No se ha encontrado ninguna clínica que contenga los términos ingresados")

#=========================================================================================================================================
# Endpoints de RATINGS:
@app.route("/ratings/<id>", methods=["GET"])
def get_rating(id):
    """
    Endpoint para obtener un rating específico de la base de datos.

    Retorna un JSON con la información del rating correspondiente al ID proporcionado
    """
    rating = db.get_or_404(Rating, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.")  # Obtiene el rating correspondiente al ID recibido
    #  Busca el handle de usuario y el nombre de clínica para los ID correspondientes, y los agrega a los datos devueltos por el JSON
    return rating_schema.jsonify(rating)  # Retorna el JSON del rating

@app.route("/ratings/<id>", methods=["DELETE"])
def delete_rating(id):
    """
    Endpoint para eliminar un rating de la base de datos.

    Elimina el rating correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    rating = db.get_or_404(Rating, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.")  # Obtiene el rating correspondiente al ID recibido
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
    rating = db.get_or_404(Rating, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.")  # Obtiene el rating existente con el ID especificado

    # Actualiza los atributos del rating con los datos proporcionados en el JSON
    rating.tipo = request.json["tipo"]
    rating.valor = request.json["valor"]
    rating.id_user = request.json["id_user"]
    rating.id_clinica = request.json["id_clinica"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return rating_schema.jsonify(rating)  # Retorna el JSON del rating actualizado

@app.route("/ratings/filter", methods=["GET"])  # Endpoint para filtrar clínicas por nombre
def filtrar_ratings():
    # extrae el término de búsqueda de los argumentos de la query
    ident = request.args.get('id_clinica', default=None, type=int)
    filt_query = db.select(Rating).where(Rating.id_clinica == ident)
    filtro_ratings = db.session.execute(filt_query).scalars()
    result = ratings_schema.dump(filtro_ratings)
    if result:
        return jsonify(result)
    else:
        abort(404, description="No se ha encontrado ningún rating que contenga los términos ingresados")

#=========================================================================================================================================
# Endpoints de USUARIOS:
@app.route("/usuarios/<id>", methods=["GET"])
def get_usuarios(id):
    """
    Endpoint para obtener un usuario específico de la base de datos.

    Retorna un JSON con la información del usuario correspondiente al ID proporcionado
    """
    usuario = db.get_or_404(Usuario, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.")  # Obtiene el usuario correspondiente al ID recibido
    return usuario_schema.jsonify(usuario)  # Retorna el JSON del usuario

@app.route("/usuarios/<id>", methods=["DELETE"])
def delete_usuario(id):
    """
    Endpoint para eliminar un usuario de la base de datos.

    Elimina el usuario correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    usuario = db.get_or_404(Usuario, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.")   # Obtiene el usuario correspondiente al ID recibido
    db.session.delete(usuario)  # Elimina el usuario de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return usuario_schema.jsonify(usuario)  # Retorna el JSON del usuario eliminado

@app.route("/usuarios", methods=["POST"])  # Endpoint para crear una clinica
def create_usuario():
    """
    Endpoint para crear un nuevo usuario en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de usuario en la base de datos.
    Retorna un JSON con la nuevo rating creado.
    """
    handle = request.json["handle"] # Obtiene el nombre del usuario del JSON proporcionado

    new_usuario = Usuario(handle)  # Crea un nuevo objeto Usuario con los datos proporcionados
    db.session.add(new_usuario)  # Agrega el nuevo usuario a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return usuario_schema.jsonify(new_usuario)  # Retorna el JSON del nuevo usuario creado

@app.route("/usuarios/<id>", methods=["PUT"])  # Endpoint para actualizar un usuario
def update_Usuario(id):
    """
    Endpoint para actualizar un usuario existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del usuario con el ID especificado.
    Retorna un JSON con el usuario actualizado.
    """
    usuario = db.get_or_404(Usuario, id, description=f"No se encontró el objeto con id '{id}' en la base de datos.") # Obtiene el usuario existente con el ID especificado

    # Actualiza los atributos del usuario con los datos proporcionados en el JSON
    usuario.handle = request.json["handle"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return usuario_schema.jsonify(usuario)  # Retorna el JSON del usuario actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de producción
    app.run(debug=True, port=5000)