from flask_sqlalchemy import SQLAlchemy
# event, me vale para los trigger. 
from sqlalchemy import event
#time delta me vale para poner trozos de tiempo, por ejemplo, en este proyecto, he puesto trozos de 5 minutos. 
from datetime import datetime
# estlas librerias son para hacer los rangos con GIST y tratar a robot como entidad física. 
from sqlalchemy.dialects.postgresql import ExcludeConstraint
# DDL es para poder pasar codigo posquesql directamende desde este script a postgres. 
# func me vale para hacer el rango desde inicio hasta fin. 
from sqlalchemy import event, DDL, func, CheckConstraint
# esto es para poder hacer el join: aliased, y que de esta manea pueda poner una tabla dentro del join. (inner join SQL).  
from sqlalchemy.orm import  aliased
from werkzeug.security import check_password_hash
# en esta lista voy a alamecenar todos los robots que no estan en servicio, para que cuando se haga la consulta de conseguir robots de un evento, me va a devolver los robots del evento, pero sin saber cual de ellos es el que está en servicio, porque 
#recoordar que esto no lo puedo guardar en la BBDD, por lo tanto en este script lo activo o desactivo y lo puede usar el script main.py para que el asistente averigue si puede manejar un robo o no. 
from estructuradatos import miListaRobotsQueNoEstanEnServicio;  
from estructuradatos import miDiccionarioEventoYasistentesDatos;  
db = SQLAlchemy();

class Administradores(db.Model):
    """
        Parmetros: 
            str: correoElectronico
            str: contrasena
    """
    __tablename__ = "miTablaAdministrador";
    __correoElectronico = db.Column(db.String(50), primary_key=True);
    __contrasena = db.Column(db.String(162), nullable=False);

    @property
    def correoElectronico (self):
        return self.__correoElectronico;
    @correoElectronico.setter
    def correoElectronico (self, value):
        self.__correoElectronico = value;
    @property
    def contrasena (self):
        return self.__contrasena;
    @contrasena.setter
    def contrasena (self, value):
        self.__contrasena = value;
        
##### funciones que menejan el evento  ##############################################################################################################################################


        
##### funciones que menejan las cuentas de los administradores  ##############################################################################################################################################


        

# esto me vale para que el indice gist funcione con enteros. 
sqlParaPoderUtilizarGistConEnteros = """CREATE EXTENSION IF NOT EXISTS btree_gist;"""
event.listen (Administradores.__table__, 'before_create', DDL(sqlParaPoderUtilizarGistConEnteros));

class Eventos (db.Model): 
    """ 
        Parmetros: 
            str: nombreDelEvento 
            date: fechaDeCreacionDelEvento 
            str: lugarDondeSeCelebra 

            str: codigoQR 
            str: administradores_correoElectronico
            str: calle 

            str: numero 
            int: codigoPostal 
    """ 
    __tablename__ = "miTablaEvento"; 
    __nombreDelEvento = db.Column (db.String (50), primary_key=True); 
    __fechaDeCreacionDelEvento = db.Column (db.DateTime, primary_key=True); 
    __lugarDondeSeCelebra = db.Column (db.String (50), primary_key=True); 
    __codigoQR = db.Column (db.String (50), nullable = False, unique=True); 
    __administradores_correoElectronico = db.Column (db.String (50), db.ForeignKey ('miTablaAdministrador._Administradores__correoElectronico', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    __calle = db.Column (db.String (50)); 
    __numero = db.Column (db.String (50)); 
    __codigoPostal = db.Column (db.Integer); 

    @property
    def nombreDelEvento (self):
        return self.__nombreDelEvento;
    @nombreDelEvento.setter
    def nombreDelEvento (self, value):
        self.__nombreDelEvento = value;
    @property
    def fechaDeCreacionDelEvento (self):
        return self.__fechaDeCreacionDelEvento;
    @fechaDeCreacionDelEvento.setter
    def fechaDeCreacionDelEvento (self, value):
        self.__fechaDeCreacionDelEvento = value;
    @property
    def lugarDondeSeCelebra (self):
        return self.__lugarDondeSeCelebra;
    @lugarDondeSeCelebra.setter
    def lugarDondeSeCelebra (self, value):
        self.__lugarDondeSeCelebra = value;
    
    @property
    def codigoQR (self):
        return self.__codigoQR;
    @codigoQR.setter
    def codigoQR (self, value):
        self.__codigoQR = value;
    @property
    def administradores_correoElectronico (self):
        return self.__administradores_correoElectronico;
    @administradores_correoElectronico.setter
    def administradores_correoElectronico (self, value):
        self.__administradores_correoElectronico = value;

    @property
    def calle (self):
        return self.__calle;
    @calle.setter
    def calle (self, value):
        self.__calle = value;
    @property
    def numero (self):
        return self.__numero;
    @numero.setter
    def numero (self, value):
        self.__numero = value;
    @property
    def codigoPostal (self):
        return self.__codigoPostal;
    @codigoPostal.setter
    def codigoPostal (self, value):
        self.__codigoPostal = value;


class Asistentes (db.Model):
    """
        Parmetros: 
            str: identificadorUnicoAsistente
            str: apodoAsistente
            str: eventos_nombreDelEvento
            date: eventos_fechaDeCreacionDelEvento
            str: eventos_lugarDondeSeCelebra
    """
    __tablename__ = "miTablaAsistente";
    __identificadorUnicoAsistente = db.Column (db.String (48), nullable = False, primary_key=True);
    __apodoAsistente = db.Column (db.String (), nullable = False, unique=True);
    __eventos_nombreDelEvento = db.Column (db.String (50), nullable=False);
    __eventos_fechaDeCreacionDelEvento = db.Column (db.DateTime,  nullable=False);
    __eventos_lugarDondeSeCelebra = db.Column (db.String (50),  nullable=False);

    __table_args__ = (db.ForeignKeyConstraint(['_Asistentes__eventos_nombreDelEvento', '_Asistentes__eventos_fechaDeCreacionDelEvento', '_Asistentes__eventos_lugarDondeSeCelebra'],['miTablaEvento._Eventos__nombreDelEvento', 'miTablaEvento._Eventos__fechaDeCreacionDelEvento', 'miTablaEvento._Eventos__lugarDondeSeCelebra'],onupdate="CASCADE", ondelete="CASCADE"),)

    @property
    def identificadorUnicoAsistente (self):
        return self.__identificadorUnicoAsistente;
    @identificadorUnicoAsistente.setter 
    def identificadorUnicoAsistente (self, value):
        self.__identificadorUnicoAsistente = value;
    @property
    def apodoAsistente (self):
        return self.__apodoAsistente;
    @apodoAsistente.setter 
    def apodoAsistente (self, value):
        self.__apodoAsistente = value;
    
    @property
    def eventos_nombreDelEvento (self):
        return self.__eventos_nombreDelEvento;
    @eventos_nombreDelEvento.setter 
    def eventos_nombreDelEvento (self, value):
        self.__eventos_nombreDelEvento = value;
    @property
    def eventos_fechaDeCreacionDelEvento (self):
        return self.__eventos_fechaDeCreacionDelEvento;
    @eventos_fechaDeCreacionDelEvento.setter 
    def eventos_fechaDeCreacionDelEvento (self, value):
        self.__eventos_fechaDeCreacionDelEvento = value;
    @property
    def eventos_lugarDondeSeCelebra (self):
        return self.__eventos_lugarDondeSeCelebra;
    @eventos_lugarDondeSeCelebra.setter 
    def eventos_lugarDondeSeCelebra (self, value):
        self.__eventos_lugarDondeSeCelebra = value;

    # esta funcion mete al asistente en la tabla de Controla. 
    def pasarAcontrolarRobot (self, parametroRobot_idRobot):
        pass;


class Robots (db.Model):
    """
        Parmetros: 
            int: idRobot
            str: macAddressDelRobot
            str: nombreDelRobot
            str: disponible
            byte: fotoDelRobot
            str: descripcionDelRobot
    """
    __tablename__ = "miTablaRobot";
    __idRobot = db.Column (db.Integer, primary_key = True);
    __macAddressDelRobot = db.Column (db.String (17), unique=True, nullable = False); 
    __nombreDelRobot = db.Column (db.String (50), unique=True, nullable = False);
    __disponible = db.Column (db.Boolean, nullable = False);
    __fotoDelRobot = db.Column (db.LargeBinary); 
    __descripcionDelRobot = db.Column (db.String (100));

    @property
    def idRobot (self):
        return self.__idRobot;
    @idRobot.setter
    def idRobot (self, value):
        self.__idRobot = value;
    @property
    def macAddressDelRobot (self):
        return self.__macAddressDelRobot;
    @macAddressDelRobot.setter
    def macAddressDelRobot (self, value):
        self.__macAddressDelRobot = value;
    @property
    def nombreDelRobot (self):
        return self.__nombreDelRobot;
    @nombreDelRobot.setter
    def nombreDelRobot (self, value):
        self.__nombreDelRobot = value;
    @property
    def disponible (self):
        return self.__disponible;
    @disponible.setter
    def disponible (self, value):
        self.__disponible = value;
    

    @property 
    def fotoDelRobot (self):
        return self.__fotoDelRobot;
    @fotoDelRobot.setter
    def fotoDelRobot (self, value):
        self.__fotoDelRobot = value;
    @property
    def descripcionDelRobot (self):
        return self.__descripcionDelRobot;
    @descripcionDelRobot.setter
    def descripcionDelRobot (self, value):
        self.__descripcionDelRobot = value;

class Vincula (db.Model):
    """
        Parmetros: 
            int: idVincula
            str: asistentes_identificadorUnicoAsistente
            str: eventos_nombreDelEvento
            date: eventos_fechaDeCreacionDelEvento
            str: eventos_lugarDondeSeCelebra
            date: fechaAcceso
            date: fechaSalida
    """
    __tablename__ = "miTablaVincula";
    idVincula = db.Column (db.Integer, primary_key = True);
    asistentes_identificadorUnicoAsistente = db.Column (db.String (48), db.ForeignKey ('miTablaAsistente._Asistentes__identificadorUnicoAsistente', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    eventos_nombreDelEvento = db.Column (db.String (50), nullable=False);
    eventos_fechaDeCreacionDelEvento = db.Column (db.DateTime,  nullable=False);
    eventos_lugarDondeSeCelebra = db.Column (db.String (50),  nullable=False);

    fechaAcceso = db.Column (db.DateTime, nullable=False);
    fechaSalida = db.Column (db.DateTime, nullable=False);

    #REQUISITO5. 
    __table_args__ = (db.ForeignKeyConstraint(['eventos_nombreDelEvento', 'eventos_fechaDeCreacionDelEvento', 'eventos_lugarDondeSeCelebra'],['miTablaEvento._Eventos__nombreDelEvento', 'miTablaEvento._Eventos__fechaDeCreacionDelEvento', 'miTablaEvento._Eventos__lugarDondeSeCelebra'],onupdate="CASCADE", ondelete="CASCADE"),
                      CheckConstraint (fechaAcceso < fechaSalida, name="miCheckConstraintFechaInicioTieneQueSerMenorQueFechaSalida"))

class DisponibleRobot (db.Model):
    """   
        Parametros: 
            int: idDisponibleRobot
            str: eventos_nombreDelEvento
            date: eventos_fechaDeCreacionDelEvento
            str:  eventos_lugarDondeSeCelebra 
            int:  robots_idRobot
            date:  fechaComienzoEnEvento
            date:  fechaFinEnEvento
    """
    __tablename__ = "mitablaDisponibleRobot";
    idDisponibleRobot = db.Column(db.Integer, primary_key=True);
    eventos_nombreDelEvento = db.Column (db.String (50), nullable=False);
    eventos_fechaDeCreacionDelEvento = db.Column (db.DateTime,  nullable=False);
    eventos_lugarDondeSeCelebra = db.Column (db.String (50),  nullable=False);
    robots_idRobot = db.Column(db.Integer, db.ForeignKey('miTablaRobot._Robots__idRobot', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    fechaComienzoEnEvento = db.Column(db.DateTime, nullable=False);
    fechaFinEnEvento = db.Column(db.DateTime, nullable=False);

    #REQUISITO4. 
    __table_args__ = (db.ForeignKeyConstraint(['eventos_nombreDelEvento', 'eventos_fechaDeCreacionDelEvento', 'eventos_lugarDondeSeCelebra'],['miTablaEvento._Eventos__nombreDelEvento', 'miTablaEvento._Eventos__fechaDeCreacionDelEvento', 'miTablaEvento._Eventos__lugarDondeSeCelebra'],onupdate="CASCADE", ondelete="CASCADE"),
                      ExcludeConstraint((robots_idRobot, '='),(func.tstzrange(func.timezone('UTC', fechaComienzoEnEvento), func.timezone('UTC', fechaFinEnEvento)), '&&'), name='miExclusionFechasYrobot_idRobotTablaDisponibleRobot', using='gist'),)


class Controla (db.Model):
    """
        parametros: 
            int: idControla
            str: asistentes_identificadorUnicoAsistente
            int: robots_idRobot
            date: fechaTomaDelRobot
            date: fechaAbandonoDelRobot
    """
    __tablename__ = "miTablaControla";
    idControla = db.Column(db.Integer, primary_key=True);
    asistentes_identificadorUnicoAsistente = db.Column (db.String (48), db.ForeignKey ('miTablaAsistente._Asistentes__identificadorUnicoAsistente', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    robots_idRobot = db.Column(db.Integer, db.ForeignKey('miTablaRobot._Robots__idRobot', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    fechaTomaDelRobot = db.Column(db.DateTime, nullable=False);
    fechaAbandonoDelRobot = db.Column(db.DateTime, nullable=False);

    #REQISITO6.  #REQUISITO7. 
    __table_args__ = (ExcludeConstraint((robots_idRobot, '='),(func.tstzrange(func.timezone('UTC', fechaTomaDelRobot), func.timezone('UTC', fechaAbandonoDelRobot)), '&&'), name='miExclusionFechasYrobot_idRobotTablaControla', using='gist'),
                      ExcludeConstraint((asistentes_identificadorUnicoAsistente, '='),(func.tstzrange(func.timezone('UTC', fechaTomaDelRobot), func.timezone('UTC', fechaAbandonoDelRobot)), '&&'), name='miExclusionFechasYasistentes_identificadorUnicoAsistente', using='gist'));

###TRIGGER################################################################################################################################################################################################
#REQUISITO9. 
@event.listens_for (Controla, 'before_insert')
# No se puedde quitar mapper, connection, de los parametro de esta función, (aunque no se instancien en ningun momento y VSC los marque como gris) ya que si no SQLalchemy da error. 
def trigger_funcion_B_I_antesDeControlarRobotRevisarRequisitos (mapper, connection, target):
    # de esta forma, del robot que quiero, consigo el evento en el que esta. 
    miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robots_idRobot==target.robots_idRobot, DisponibleRobot.fechaComienzoEnEvento<=datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).first();
    # esto significa que el robot que quiero, no esta asociado a ningun evento. 
    if (miDisponibleRobot == None):
        raise Exception ("exception.B_I. Ese robot no esta en ningun evento.");
    # en este caso he obtenido el evento en el que esta asociado ese robot actualmente, es decir, tengo los datos del evento en el que esta. 
    else:
        # lo que voy a hacer es comprobar si ese asistente está asociando a ese evento. 
        miVincula = Vincula.query.filter_by (asistentes_identificadorUnicoAsistente=target.asistentes_identificadorUnicoAsistente, eventos_nombreDelEvento=miDisponibleRobot.eventos_nombreDelEvento, eventos_fechaDeCreacionDelEvento=miDisponibleRobot.eventos_fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=miDisponibleRobot.eventos_lugarDondeSeCelebra). first ();
        # esto significa que el asistente, no está asociado al evento
        if (miVincula == None): 
            raise Exception ("exception.B_I. Ese asistente, no está en ese evento en el cual se ha solicitado ese robot. ");
        else: 
            # en el caso de que la fecha de comienzo y fin en evento, no abarque a la fecha de toma y abandono del robot, entonces no se puede controlar ese robot. 
            if ((miDisponibleRobot.fechaComienzoEnEvento > target.fechaTomaDelRobot) or (miDisponibleRobot.fechaFinEnEvento < target.fechaAbandonoDelRobot)):
                raise Exception ("exception.B_I. Ese robot y ese asistente, sí etan en ese evento, pero le fecha en la que ta el robot en el evento, no abarca la fecha en la que ese asistente maneja ese robot. ");
                





