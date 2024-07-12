
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy();

class LugarDelEvento (db.Model):
    __tablename__ = "miTablaLugarDelEvento";
    idLugarDelEvento = db.Column (db.Integer, primary_key = True);
    calle = db.Column (db.String (50), nullable=False);
    numero = db.Column (db.String (50), nullable=False);
    codigoPostal = db.Column (db.Integer);
    edificioDondeSeCelebra = db.Column (db.String (50), nullable=False);
    # esto no es un atributo, sino una relacion. 
    lugarDelEvento_idLugarDelEvento_relacionEvento = db.relationship ('Evento', backref='lugarDelEvento_idLugarDelEvento_relacionEvento');

class Evento (db.Model):
    __tablename__ = "miTablaEvento";
    idEvento = db.Column (db.Integer, primary_key = True);
    nombreDelEvento = db.Column (db.String (50), nullable=False, unique=True);
    fechaDeCreacionDelEvento = db.Column (db.DateTime);
    lugarDelEvento_idLugarDelEvento = db.Column (db.Integer, db.ForeignKey ('miTablaLugarDelEvento.idLugarDelEvento'), nullable=False);
    # esto no es un atributo, sino una relacion. 
    evento_idEvento_relacionAsistente = db.relationship('Asistente');
    evento_idEvento_relacionRobot = db.relationship ('Robot');

class Asistente (db.Model):
    __tablename__ = "miTablaAsistente";
    tokenDeSesion = db.Column (db.String (48), primary_key = True); #el token de sesion del navegador tiene 135 caracteres. 
    apodo = db.Column (db.String (50));
    descripcionDelAsistente = db.Column (db.String (100));
    posicionDeColaConFecha = db.Column (db.DateTime);   
    evento_idEvento = db.Column (db.Integer, db.ForeignKey('miTablaEvento.idEvento'), nullable=False);
    asistente_tokenDeSesion_relacionRobot = db.relationship ('Robot');
    fechaDeAccesoAlSistema = db.Column (db.DateTime, nullable=False);   


class Robot (db.Model):
    __tablename__ = "miTablaRobot";
    idRobot = db.Column (db.Integer, primary_key = True);
    MACaddressDelRobot = db.Column (db.String (12), unique=True, nullable = False); 
    nombreDelRobot = db.Column (db.String (50), unique=True, nullable = False);
    fotoDelRobot = db.Column (db.LargeBinary);
    evento_idEvento = db.Column (db.Integer, db.ForeignKey ('miTablaEvento.idEvento'), nullable = True);
    asistente_tokenDeSesion = db.Column (db.String (48), db.ForeignKey ('miTablaAsistente.tokenDeSesion'), nullable = True, unique = True);
    robotEnServicio = db.Column (db.Boolean, nullable = False);   
    descripcionDelRobot = db.Column (db.String (100));

class Administrador (db.Model):
    __tablename__ = "miTablaAdministrador";
    correoElectronico = db.Column (db.String (50), primary_key = True);
    contrasena = db.Column (db.String (162), nullable = False);
    def validarContrasena (self, password):
        return True;


