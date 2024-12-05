from flask_sqlalchemy import SQLAlchemy
# event, me vale para los trigger. 
from sqlalchemy import event
#time delta me vale para poner trozos de tiempo, por ejemplo, en este proyecto, he puesto trozos de 5 minutos. 
from datetime import datetime, timedelta
# estlas librerias son para hacer los rangos con GIST y tratar a robot como entidad física. 
from sqlalchemy.dialects.postgresql import ExcludeConstraint
# DDL es para poder pasar codigo posquesql directamende desde este script a postgres. 
# func me vale para hacer el rango desde inicio hasta fin. 
from sqlalchemy import event, DDL, func, CheckConstraint
# esto es para poder hacer el join: aliased, y que de esta manea pueda poner una tabla dentro del join. (inner join SQL).  
from sqlalchemy.orm import  aliased
from werkzeug.security import check_password_hash



db = SQLAlchemy();

class Administradores(db.Model):
    """
        Parmetros: 
            str: correoElectronico
            str: contrasena
    """
    __tablename__ = "miTablaAdministrador";
    _correoElectronico = db.Column(db.String(50), primary_key=True);
    _contrasena = db.Column(db.String(162), nullable=False);


    def validarContrasena (self, password):
        miContrasenaConHash = self._contrasena;
        if (check_password_hash(miContrasenaConHash, password)):
            return True;
        else:
            return False;
        
##### funciones que gestionan los robots######################################################################################################################################################################################################################
    def funcion_crearRobot (self, parametroMacAddressDelRobot, parametroNombreDelRobot, parametroFotoDelRobot=None, parametroDescripcionDelRobot=None):
        miRobots = Robots (_macAddressDelRobot=parametroMacAddressDelRobot, _nombreDelRobot=parametroNombreDelRobot, _fotoDelRobot=parametroFotoDelRobot, _descripcionDelRobot=parametroDescripcionDelRobot);
        db.session.add (miRobots);
        db.session.commit ();
    

    def funcion_modificarRobot (self, parametroIdRobot, parametroMacAddressDelRobot=None, parametroNombreDelRobot=None, parametroFotoDelRobot=None, parametroDescripcionDelRobot=None):
        miRobots = Robots.query.filter_by (_idRobot = parametroIdRobot).first();

        if (parametroMacAddressDelRobot != None) and (parametroMacAddressDelRobot != miRobots._macAddressDelRobot):
            miRobots._macAddressDelRobot = parametroMacAddressDelRobot;
        
        if (parametroNombreDelRobot != None) and (parametroNombreDelRobot != miRobots._nombreDelRobot):
            miRobots._nombreDelRobot = parametroNombreDelRobot;
        
        if (parametroFotoDelRobot != None) and (parametroFotoDelRobot != miRobots._fotoDelRobot):
            miRobots._fotoDelRobot = parametroFotoDelRobot;
        
        if (parametroDescripcionDelRobot != None) and (parametroDescripcionDelRobot != miRobots._descripcionDelRobot):
            miRobots._descripcionDelRobot = parametroDescripcionDelRobot;
        
        db.session.commit ();

    

    def funcion_borrarRobot (self, parametroIdRobot):
        miRobots = Robots.query.filter_by (_idRobot=parametroIdRobot).first ();
        db.session.delete (miRobots);
        db.session.commit ();
    
    #recordar que desactivar un robot, hace que se expulse al asistente del robot, es decir, que lo deje de controlar. 
    def funcion_activarOdesactivarRobot (self, parametroIdRobot, parametroEnServicio):
        # solamente en el caso de que lo este quitando del servicio, es cuando tengo que ver si hay algun asistente que este controlando ese robot. 
        if (parametroEnServicio == False):
            miControla = Controla.query.filter (Controla.robots_idRobot == parametroIdRobot, Controla.fechaTomaDelRobot <= datetime.now(), Controla.fechaAbandonoDelRobot >= datetime.now()).first ();
            if (miControla):
                miControla.fechaAbandonoDelRobot = datetime.now ();
                db.session.commit ();

        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now(), DisponibleRobot.robots_idRobot == parametroIdRobot).first();
        miDisponibleRobot.disponible = parametroEnServicio;
        db.session.commit ();
    
    def funcion_conseguirTodosLosRobots (self):
        return Robots.query.all();


    def funcion_conseguirTodosLosRobotsQueNoSonDeEseEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        # lo que hago primero es obtener todos los Disponible robot que estan en el evento. 
        miListaDisponibleRobotQueEstaEnElEvento = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra).all (); 
    
        # aqui lo que hago es de los disponibleRobot que estan asignados al evento, los conivierto a Robot, para saber que robots son los que sí estan cogidos. 
        miListaRobotQueSeEstanUsando = [];
        for i in miListaDisponibleRobotQueEstaEnElEvento:
            miRobot = Robots.query.filter_by (_idRobot=i.robots_idRobot).first ();
            if (miRobot not in miListaRobotQueSeEstanUsando):
                miListaRobotQueSeEstanUsando.append (miRobot);
    
        # obtengo todos los robots del sistema. 
        miListaRobotTodos = Robots.query.all();
    
        #en esta parte lo que hago es que a la lista que almacena todos los robots del sistema, le resto los robots que sí que están en el evento. 
        for i in miListaRobotTodos[:]:
            if (i in miListaRobotQueSeEstanUsando):
                miListaRobotTodos.remove (i);
        return miListaRobotTodos;

    def funcion_conseguirRobotPorIdRobot (self, parametroIdRobot):
        return Robots.query.filter_by (_idRobot=parametroIdRobot).first();

    def funcion_conseguirRobotsQueNoEstanEnNingunEvento (self):
        miDisponibleRobotAlias = aliased (DisponibleRobot);
        return db.session.query(Robots).outerjoin (miDisponibleRobotAlias, Robots._idRobot == miDisponibleRobotAlias.robots_idRobot).filter (miDisponibleRobotAlias.robots_idRobot==None).all ();

    def funcion_verSiPuedoBorrarRobot (self, paramametroIdRobot):
        miVerdadPuedoBorrarRobot = True;
        miEventoAlias = aliased (Eventos);
        miDisponibleRobot = db.session.query(DisponibleRobot).join (miEventoAlias, DisponibleRobot.eventos_nombreDelEvento==miEventoAlias._nombreDelEvento and DisponibleRobot.eventos_fechaDeCreacionDelEvento==miEventoAlias._fechaDeCreacionDelEvento and DisponibleRobot.eventos_lugarDondeSeCelebra==miEventoAlias._lugarDondeSeCelebra).filter (DisponibleRobot.robots_idRobot==paramametroIdRobot, miEventoAlias._administradores_correoElectronico!=self._correoElectronico).first();  
        if (miDisponibleRobot):
            # en este caso como sí que ha encontrado un disponibleRobot, entonces eso signigfica que otro adminsitrador es dueño tambien de ese robot, por lo tanto, no se va a poder eliminar. Se va a dejar en False. 
            miVerdadPuedoBorrarRobot = False;

        return miVerdadPuedoBorrarRobot;

    def funcion_verSiPuedoModificarRobot (self, paramametroIdRobot):
        miVerdadPuedoModificarRobot = True;
        # en este punto veo si en el momento actual del sistema el robot esta en un evento, es decir está en la tabla de disponibleRobot. 
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robots_idRobot==paramametroIdRobot, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).first();
        # aqhui he coprobado que es verdad que el robot en el momento actual, esta en un evento por lo tanto  dentro de este if voy a averiguar que evento es, para del evento sacar quien es el administrador. 
        if (miDisponibleRobot):
            miEventos = Eventos.query.filter_by (_nombreDelEvento=miDisponibleRobot.eventos_nombreDelEvento, _fechaDeCreacionDelEvento=miDisponibleRobot.eventos_fechaDeCreacionDelEvento, _lugarDondeSeCelebra=miDisponibleRobot.eventos_lugarDondeSeCelebra).first ();
            # aqui comparo el administrador dueño del evento con el administrador que ha sido instanciodo, para devolver si puedo o no modificar ese robot.  En el caso de que no sean los mismos, entonces significa que otro administrador
            # tiene en un evento actualmente ese robot, por lo tanto el administrador que ha isntaciado la clase no puede tocar sus parametros, se devolverá False. 
            if (miEventos._administradores_correoElectronico != self._correoElectronico):
                miVerdadPuedoModificarRobot = False;
    
        return miVerdadPuedoModificarRobot;


    def funcion_verSiUnRobotEstaEnAlMenosUnEvento (self, parametroIdRobot):
        miVerdadVerSiEseRobotEstaEnAlmenosUnEvento = False;
        miDisponibleRobot = DisponibleRobot.query.filter_by (robots_idRobot = parametroIdRobot).first ();
        if (miDisponibleRobot):
            miVerdadVerSiEseRobotEstaEnAlmenosUnEvento = True;
        return miVerdadVerSiEseRobotEstaEnAlmenosUnEvento;

    def funcion_conseguirRobotsQueUsoEnEventosAdministrador (self):
        miListaEventos = Eventos.query.filter_by (_administradores_correoElectronico = self._correoElectronico).all();
        miListaRobots = [];
        for i in miListaEventos:
            miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento == i._nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento == i._fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra == i._lugarDondeSeCelebra).all();
            for j in miListaDisponibleRobot:
                miRobots = Robots.query.filter_by (_idRobot = j.robots_idRobot).first ();
                if (miRobots not in miListaRobots):
                    miListaRobots.append (miRobots);
        return miListaRobots;

    def funcion_conseguirListaDisponibleRobotEventosDelAdministradorSinServicioActualmente (self):
        miListaEventos = Eventos.query.filter_by (_administradores_correoElectronico= self._correoElectronico).all();
        miListaDisponibleRobotSinServicioActualmente = [];
        for i in miListaEventos:
            miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento == i._nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento == i._fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra == i._lugarDondeSeCelebra,
                                                                   DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now(), DisponibleRobot.disponible == False).all();
            for j in miListaDisponibleRobot:
                miListaDisponibleRobotSinServicioActualmente.append (j);
        return miListaDisponibleRobotSinServicioActualmente;

    def funcion_conseguirListaEventosQueTienenAlmenosUnRobotEsperandoPorAsistentes (self):
        miListaEventos = [];
        miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();
        for i in miListaDisponibleRobot:
            miEventos = Eventos.query.filter (Eventos._nombreDelEvento == i.eventos_nombreDelEvento, Eventos._fechaDeCreacionDelEvento == i.eventos_fechaDeCreacionDelEvento, Eventos._lugarDondeSeCelebra == i.eventos_lugarDondeSeCelebra).first();
            if miEventos not in miListaEventos:
                miListaEventos.append (miEventos);
        return  miListaEventos;



##### funciones que menejan el evento  ######################################################################################################################################################################################################################
    def funcion_conseguirEventoPorClavePrimaria (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        return Eventos.query.filter (Eventos._nombreDelEvento == parametroNombreDelEvento, Eventos._fechaDeCreacionDelEvento == parametroFechaDeCreacionDelEvento, Eventos._lugarDondeSeCelebra == parametroLugarDondeSeCelebra).first ();

    def funcion_crearEvento (self, parametroNombreDelEvento, parametroLugarDondeSeCelebra, parametroCodigoQR=None, parametroCalle = None, parametroNumero = None, parametroCodigoPostal = None):
        miFechaDeCreaacionDelEvento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S");
        if (parametroCodigoQR != None) and (parametroCodigoQR != ""):
            miVariableCodigoQR = parametroCodigoQR;
        else:
            miVariableCodigoQR = parametroNombreDelEvento +miFechaDeCreaacionDelEvento +parametroLugarDondeSeCelebra;  
        miEventos = Eventos (_nombreDelEvento=parametroNombreDelEvento, _fechaDeCreacionDelEvento=miFechaDeCreaacionDelEvento, _lugarDondeSeCelebra=parametroLugarDondeSeCelebra, _codigoQR=miVariableCodigoQR, _administradores_correoElectronico=self._correoElectronico, _calle=parametroCalle, _numero=parametroNumero,  _codigoPostal=parametroCodigoPostal);
        db.session.add (miEventos);
        db.session.commit ();

    def funcion_conseguirTodosLosEventos (self):
        return Eventos.query.all();

    def funcion_conseguirTodosLosEventosDeEseAdministrador (self):
        return Eventos.query.filter_by (_administradores_correoElectronico=self._correoElectronico).all();

    def funcion_conseguirTodosLosEventosPorCorreoElectronico (self, parametroCorreoElectronico):
        return Eventos.query.filter_by (_administradores_correoElectronico = parametroCorreoElectronico).all();

    def funcion_conseguirDisponibleRobotPorEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        return DisponibleRobot.query.filter_by (eventos_nombreDelEvento=parametroNombreDelEvento, eventos_fechaDeCreacionDelEvento=parametroFechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=parametroLugarDondeSeCelebra).all();


    def funcion_conseguirDisponibleRobotPorEventoYporEstarContempladaLaFechaDelSistema (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        miListaDisponibleRobot = [];
        miListaDisponibleRobotQueActualmenteEstanEnElEvento= DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();
        for i in miListaDisponibleRobotQueActualmenteEstanEnElEvento:
            miListaDisponibleRobot.append (i);
            # en esta primera parte, cojo de ese mismo robot en ese mismo eventos, los eventos que ya han pasado. 
            miListaDisponibleRobot += DisponibleRobot.query.filter (DisponibleRobot.robots_idRobot == i.robots_idRobot, DisponibleRobot.fechaFinEnEvento < datetime.now(), DisponibleRobot.eventos_nombreDelEvento == parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra).all();
            # # en esta primera parte, cojo de ese mismo robot en ese mismo eventos, los eventos que van a pasar. 
            miListaDisponibleRobot += DisponibleRobot.query.filter (DisponibleRobot.robots_idRobot == i.robots_idRobot, DisponibleRobot.fechaComienzoEnEvento > datetime.now(), DisponibleRobot.eventos_nombreDelEvento == parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra).all();
        return miListaDisponibleRobot;

    def funcion_conseguirDisponibleRobotPorEventoYporNoEstarContempladaLaFechaDelSistema (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        # primero lo que hago es obtener todos los robots que esten en la tabla de disponibleRobot que no contengan la fecha del sistema, para que despues a estos, como es logico, puede ser que haya algun robot (o algun disponibleRobot) que sí contenga la fecha del sistema, entonces restarles los que sí estan contemplados. 
        miListaDisponibleRobotQueActualmenteNoEstanEnElEvento = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra, DisponibleRobot.fechaComienzoEnEvento > datetime.now()).all();
        miListaDisponibleRobotQueActualmenteNoEstanEnElEvento += DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra, DisponibleRobot.fechaComienzoEnEvento < datetime.now()).all();
        miListaDisponibleRobotQueActualmenteEstanEnElEvento= DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();

        # en esta parte para restar a los disponibleRobot que no tienen contemplada la fecha del sistema, los disponibleRobot que sí que la tienen contemplada, voy a crear esta lista de enteros del robots_idRobot, para que despues un bucle for sea el que busque en esta lista de enteros, de manera mas entendible. 
        milistaDeEnterosRobot_idRobot = [];
        for i in miListaDisponibleRobotQueActualmenteEstanEnElEvento:
            milistaDeEnterosRobot_idRobot.append (i.robots_idRobot);
        for i in miListaDisponibleRobotQueActualmenteNoEstanEnElEvento[:]:
            if (i.robots_idRobot in milistaDeEnterosRobot_idRobot):
                miListaDisponibleRobotQueActualmenteNoEstanEnElEvento.remove (i);
        return miListaDisponibleRobotQueActualmenteNoEstanEnElEvento;

    def funcion_conseguirDisponibleRobotPorIdRobotYporEstarContempladaLaFechaDelSistema (self, parametroIdRobot):
        return DisponibleRobot.query.filter (DisponibleRobot.fechaComienzoEnEvento <= datetime.now (), DisponibleRobot.fechaFinEnEvento >= datetime.now(), DisponibleRobot.robots_idRobot == parametroIdRobot).first ();


    def funcion_modificarDatosDelEvento (self, parametroAntiguoNombreDelEvento, parametroAntiguoFechaDeCreacionDelEvento, parametroAntiguoLugarDondeSeCelebra, parametroNombreDelEvento, parametroLugarDondeSeCelebra, parametroCodigoQR=None, parametroCalle=None, parametroNumero=None, parametroCodigoPostal=None):
        miEventos = Eventos.query.filter (Eventos._nombreDelEvento == parametroAntiguoNombreDelEvento, Eventos._fechaDeCreacionDelEvento == parametroAntiguoFechaDeCreacionDelEvento, Eventos._lugarDondeSeCelebra == parametroAntiguoLugarDondeSeCelebra).first ();
        miVariableMensajeDeError = None;
        if (miEventos._codigoQR != parametroCodigoQR):
            # en el caso de que el código QR recién modificado esté ya en la BBDD, devuelvo una exception. 
            if (Eventos.query.filter_by (_codigoQR = parametroCodigoQR).first ()):
                miVariableMensajeDeError = ("exception. Esa URL para ese evento ya existe en la base de datos, recuerde que el link de cade evento debe de ser distinto. ");
                return miVariableMensajeDeError;
        miEventos._nombreDelEvento = parametroNombreDelEvento;
        miEventos._lugarDondeSeCelebra = parametroLugarDondeSeCelebra
        if (parametroCodigoQR != None) and (parametroCodigoQR != "") and (miEventos._codigoQR != parametroCodigoQR):
            miEventos._codigoQR =  parametroCodigoQR;
        if (parametroCalle != None) and (miEventos._calle != parametroCalle):
            miEventos._calle = parametroCalle;
        if (parametroNumero != None) and (miEventos._numero != parametroNumero):
            miEventos._numero = parametroNumero;
        if (parametroCodigoPostal != None) and (miEventos._codigoPostal != parametroCodigoPostal):
            miEventos._codigoPostal = parametroCodigoPostal;
        db.session.commit ();
        return miVariableMensajeDeError;
    
    def funcion_modificarRobotDelEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento, parametroNuevaFechaComienzoEnEvento=None, parametroNuevaFechaFinEnEvento=None, parametroEnServicio=None):
        miVariableDisponible = False;
        miVariableMensajeDeError = None;
        if (parametroEnServicio == "on"):
            miVariableDisponible = True;
        
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra, 
                                                          DisponibleRobot.robots_idRobot==parametroRobot_idRobot, DisponibleRobot.fechaComienzoEnEvento==parametroFechaComienzoEnEvento, DisponibleRobot.fechaFinEnEvento == parametroFechaFinEnEvento).first();

        if (parametroNuevaFechaComienzoEnEvento != ""):
            # en el caso de que se modifique la fecha de un robot en el día enterior, entonces no dejo que se modifique la fecha de ese robot en ese evento.  
            if (parametroNuevaFechaComienzoEnEvento < (datetime.now().strftime ("%Y-%m-%d"))): 
                miVariableMensajeDeError = ("exception. No se puede modificar la fecha de ese robot en el evento, está estableciendo la fecha de comienzo en un día que ya pasó.  ");
                return miVariableMensajeDeError;
            else:
                miDisponibleRobot.fechaComienzoEnEvento = parametroNuevaFechaComienzoEnEvento;
                if (parametroNuevaFechaFinEnEvento != ""):
                    miDisponibleRobot.fechaFinEnEvento = parametroNuevaFechaFinEnEvento;
                else:
                    miDisponibleRobot.fechaFinEnEvento = parametroFechaFinEnEvento;
        else:
            if (parametroNuevaFechaFinEnEvento != ""):
                miDisponibleRobot.fechaComienzoEnEvento = parametroFechaDeCreacionDelEvento;
                miDisponibleRobot.fechaFinEnEvento = parametroFechaFinEnEvento;
        
        miDisponibleRobot.disponible = miVariableDisponible;
        db.session.commit ();
        return miVariableMensajeDeError;
        

    
    def funcion_sumarRobotAlEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento, parametroEnServicio=None):
        miVariableMensajeDeError = None;

        # en el caso de que se sume un robot en el día enterior, entonces no dejo que se meta ese robot en el evento. 
        if (parametroFechaComienzoEnEvento < (datetime.now().strftime ("%Y-%m-%d"))): 
            miVariableMensajeDeError = ("exception. No se puede sumar ese robot al evento, está simando ese robot al evento en un día pasado.  ");
            return miVariableMensajeDeError;
    
        miVariableDisponible = False;
        if (parametroEnServicio == "on"):
            miVariableDisponible = True;

        miDisponibleRobot = DisponibleRobot (eventos_nombreDelEvento=parametroNombreDelEvento, eventos_fechaDeCreacionDelEvento=parametroFechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=parametroLugarDondeSeCelebra, 
                                             robots_idRobot=parametroRobot_idRobot, fechaComienzoEnEvento = parametroFechaComienzoEnEvento, fechaFinEnEvento = parametroFechaFinEnEvento, disponible = miVariableDisponible);
        db.session.add (miDisponibleRobot);
        db.session.commit ();
        return miVariableMensajeDeError;
    
    def funcion_eliminarRobotDelEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento):
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==parametroLugarDondeSeCelebra, 
                                                          DisponibleRobot.robots_idRobot==parametroRobot_idRobot, DisponibleRobot.fechaComienzoEnEvento==parametroFechaComienzoEnEvento, DisponibleRobot.fechaFinEnEvento == parametroFechaFinEnEvento).first();
        db.session.delete (miDisponibleRobot);
        db.session.commit ();
    
    def funcion_borrarEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        miEventos = Eventos.query.filter (Eventos._nombreDelEvento==parametroNombreDelEvento, Eventos._fechaDeCreacionDelEvento==parametroFechaDeCreacionDelEvento, Eventos._lugarDondeSeCelebra==parametroLugarDondeSeCelebra).first ();
        db.session.delete (miEventos);
        db.session.commit();

    # con esta funcion lo que hago es comprobar si el administrdor que ha pulsado en el evento, es o no el administrador, lo que pasa es que a un administrador nunca se le van a mostrar los eventos que no son suyos, pero en el caso de que 
    #conozca el nombre, la fecha y el lugar de un evento que no es suyo, lo que va a pasar es que si el lo pone en la URL, va a poder hacer modificaciones sobre este evento, y eso es algo que yo no quiero, por lo tanto cada vez que se vaya  a conseguir un 
    # evento, lo que voy a hacer aqu es comprobar si ese evento es o no de ese administrador. 
    def funcion_verSiEseEventoEsDeEseAdministrador (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        miVerdadVerSiEseEventoEsDeEseAdministrador = True; 
        miEventos = Eventos.query.filter (Eventos._nombreDelEvento == parametroNombreDelEvento, Eventos._fechaDeCreacionDelEvento == parametroFechaDeCreacionDelEvento, Eventos._lugarDondeSeCelebra == parametroLugarDondeSeCelebra, Eventos._administradores_correoElectronico == self._correoElectronico).first(); 
        if (miEventos == None):
            miVerdadVerSiEseEventoEsDeEseAdministrador = False; 
        return miVerdadVerSiEseEventoEsDeEseAdministrador;


##### funciones que menejan las cuentas de los administradores  ##############################################################################################################################################################################################
    
    def funcion_conseguirTodasLasCuentasMenosLaInstanciada (self):
        return Administradores.query.filter (Administradores._correoElectronico != self._correoElectronico).all ();

    def funcion_borrarCuentaAdministrador (self, parametroCorreoElectronico):
        miAdministradores = Administradores.query.filter_by (_correoElectronico = parametroCorreoElectronico).first ();
        db.session.delete (miAdministradores);
        db.session.commit ();

##### funciones que menejan los asistentes de los eventos  ##############################################################################################################################################################################################

    def funcion_conseguirTodosLosAsistentesDelSistema (self):
        return Asistentes.query.all ();

    def funcion_conseguirTodosLosAsistentesDelAdministrador (self):
        miListaEventos = Eventos.query.filter_by (_administradores_correoElectronico = self._correoElectronico).all ();
        miListaAsistentes = [];
        for i in miListaEventos:
            miListaVincula = Vincula.query.filter (Vincula.eventos_nombreDelEvento == i._nombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == i._fechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == i._lugarDondeSeCelebra).all();
            for j in miListaVincula: 
                if (j.asistentes_identificadorUnicoAsistente not in miListaAsistentes):
                    miListaAsistentes.append (j.asistentes_identificadorUnicoAsistente);
        return miListaAsistentes;

    def funcion_conseguirPorcentajeAsistentesQueSiHanControladoUnRobot (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        miPorcentajeAsistentesQueSiHanControladoUnRobot = 0;
        miListaAsistentesQueSiHanControladoUnRobot = [];
        miListaVincula = Vincula.query.filter (Vincula.eventos_nombreDelEvento == parametroNombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == parametroFechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == parametroLugarDondeSeCelebra).all();
        # esto es para evitar ele error de división entre cero, ya que si no hay ningún asistente vinculado a mi evento, entonces no tiene sentido sacar el porcentaje de los que han utilizado ya un robot. 
        if (len (miListaVincula) == 0):
            return 0;
        else:
            miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento == parametroNombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento == parametroFechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra == parametroLugarDondeSeCelebra).all();
            for i in miListaVincula:
                miListaControla = Controla.query.filter_by (asistentes_identificadorUnicoAsistente =i.asistentes_identificadorUnicoAsistente).all ();
                for j in miListaControla: 
                    for k in miListaDisponibleRobot:
                        # en este momento compruebo que ese asistenete que esta en la tabla controla, su controla se corresponde con algun disponibleRobot de la lista que se ha extraido con ese evento, entonces determino que sí ha controlado al menos un robot
                        # en algún determinado momento. 
                        if (j.robots_idRobot == k.robots_idRobot) and (j.fechaTomaDelRobot >= k.fechaComienzoEnEvento) and (j.fechaAbandonoDelRobot <= k.fechaFinEnEvento):
                            miListaAsistentesQueSiHanControladoUnRobot.append (i.asistentes_identificadorUnicoAsistente);
                            break;
        
            miPorcentajeAsistentesQueSiHanControladoUnRobot = len (miListaAsistentesQueSiHanControladoUnRobot) / len (miListaVincula);
            miPorcentajeAsistentesQueSiHanControladoUnRobot = miPorcentajeAsistentesQueSiHanControladoUnRobot * 100;
            miPorcentajeAsistentesQueSiHanControladoUnRobot = round (miPorcentajeAsistentesQueSiHanControladoUnRobot, 2);
            return miPorcentajeAsistentesQueSiHanControladoUnRobot;

    def funcion_conseguirTodosLosAsistentesVinculadosAlEvento (self, parametroNombreDelEvento, parametroFechaDeCreacionDelEvento, parametroLugarDondeSeCelebra):
        return Vincula.query.filter (Vincula.eventos_nombreDelEvento == parametroNombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == parametroFechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == parametroLugarDondeSeCelebra).all();


##### Fin de la clase administradores.  ######################################################################################################################################################################################################################

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
    _nombreDelEvento = db.Column (db.String (50), primary_key=True); 
    _fechaDeCreacionDelEvento = db.Column (db.DateTime, primary_key=True); 
    _lugarDondeSeCelebra = db.Column (db.String (50), primary_key=True); 
    _codigoQR = db.Column (db.String (200), nullable = False, unique=True); 
    _administradores_correoElectronico = db.Column (db.String (50), db.ForeignKey ('miTablaAdministrador._correoElectronico', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    _calle = db.Column (db.String (50)); 
    _numero = db.Column (db.String (50)); 
    _codigoPostal = db.Column (db.Integer); 


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
    _identificadorUnicoAsistente = db.Column (db.String (48), nullable = False, primary_key=True);
    _apodoAsistente = db.Column (db.String (), nullable = False, unique=True);

    # esta funcion mete al asistente en la tabla de Controla. 
    def pasarAcontrolarRobot (self, parametroidentIficadorUnicoAsistente, parametroIdRobot):
        miControla = Controla (asistentes_identificadorUnicoAsistente = parametroidentIficadorUnicoAsistente, robots_idRobot = parametroIdRobot, fechaTomaDelRobot = datetime.now(), fechaAbandonoDelRobot = datetime.now() + timedelta(minutes=5));
        db.session.add (miControla);
        db.session.commit ();

    def funcion_consultaEvento (self, parametroRobot_idRobot):
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robots_idRobot == parametroRobot_idRobot, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).first ();
        return Eventos.query.filter (Eventos._nombreDelEvento == miDisponibleRobot.eventos_nombreDelEvento, Eventos._fechaDeCreacionDelEvento == miDisponibleRobot.eventos_fechaDeCreacionDelEvento, Eventos._lugarDondeSeCelebra == miDisponibleRobot.eventos_lugarDondeSeCelebra).first ();

    def funcion_consultaRobot (self, parametroIdRobot):
        return Robots.query.filter_by (_idRobot = parametroIdRobot).first();

class Robots (db.Model):
    """
        Parmetros: 
            int: idRobot
            str: macAddressDelRobot
            str: nombreDelRobot
            byte: fotoDelRobot
            str: descripcionDelRobot
    """
    __tablename__ = "miTablaRobot";
    _idRobot = db.Column (db.Integer, primary_key = True);
    _macAddressDelRobot = db.Column (db.String (17), unique=True, nullable = False); 
    _nombreDelRobot = db.Column (db.String (50), unique=True, nullable = False);
    _fotoDelRobot = db.Column (db.LargeBinary); 
    _descripcionDelRobot = db.Column (db.String (100));


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
    asistentes_identificadorUnicoAsistente = db.Column (db.String (48), db.ForeignKey ('miTablaAsistente._identificadorUnicoAsistente', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    eventos_nombreDelEvento = db.Column (db.String (50), nullable=False);
    eventos_fechaDeCreacionDelEvento = db.Column (db.DateTime,  nullable=False);
    eventos_lugarDondeSeCelebra = db.Column (db.String (50),  nullable=False);

    fechaAcceso = db.Column (db.DateTime, nullable=False);
    fechaSalida = db.Column (db.DateTime, nullable=False);

    #REQUISITO5. 
    __table_args__ = (db.ForeignKeyConstraint(['eventos_nombreDelEvento', 'eventos_fechaDeCreacionDelEvento', 'eventos_lugarDondeSeCelebra'],['miTablaEvento._nombreDelEvento', 'miTablaEvento._fechaDeCreacionDelEvento', 'miTablaEvento._lugarDondeSeCelebra'],onupdate="CASCADE", ondelete="CASCADE"),
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
            str: disponible
    """
    __tablename__ = "mitablaDisponibleRobot";
    idDisponibleRobot = db.Column(db.Integer, primary_key=True);
    eventos_nombreDelEvento = db.Column (db.String (50), nullable=False);
    eventos_fechaDeCreacionDelEvento = db.Column (db.DateTime,  nullable=False);
    eventos_lugarDondeSeCelebra = db.Column (db.String (50),  nullable=False);
    robots_idRobot = db.Column(db.Integer, db.ForeignKey('miTablaRobot._idRobot', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    fechaComienzoEnEvento = db.Column(db.DateTime, nullable=False);
    fechaFinEnEvento = db.Column(db.DateTime, nullable=False);
    disponible = db.Column (db.Boolean, nullable = False);

    #REQUISITO4. 
    __table_args__ = (db.ForeignKeyConstraint(['eventos_nombreDelEvento', 'eventos_fechaDeCreacionDelEvento', 'eventos_lugarDondeSeCelebra'],['miTablaEvento._nombreDelEvento', 'miTablaEvento._fechaDeCreacionDelEvento', 'miTablaEvento._lugarDondeSeCelebra'],onupdate="CASCADE", ondelete="CASCADE"),
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
    asistentes_identificadorUnicoAsistente = db.Column (db.String (48), db.ForeignKey ('miTablaAsistente._identificadorUnicoAsistente', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    robots_idRobot = db.Column(db.Integer, db.ForeignKey('miTablaRobot._idRobot', onupdate="CASCADE", ondelete="CASCADE"), nullable=False);
    fechaTomaDelRobot = db.Column(db.DateTime, nullable=False);
    fechaAbandonoDelRobot = db.Column(db.DateTime, nullable=False);

    #REQISITO6.  #REQUISITO7. 
    __table_args__ = (ExcludeConstraint((robots_idRobot, '='),(func.tstzrange(func.timezone('UTC', fechaTomaDelRobot), func.timezone('UTC', fechaAbandonoDelRobot)), '&&'), name='miExclusionFechasYrobot_idRobotTablaControla', using='gist'),
                      ExcludeConstraint((asistentes_identificadorUnicoAsistente, '='),(func.tstzrange(func.timezone('UTC', fechaTomaDelRobot), func.timezone('UTC', fechaAbandonoDelRobot)), '&&'), name='miExclusionFechasYasistentes_identificadorUnicoAsistente', using='gist'));

###TRIGGER################################################################################################################################################################################################################################################
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
                





