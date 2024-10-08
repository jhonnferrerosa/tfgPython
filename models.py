
from flask_sqlalchemy import SQLAlchemy

# event, me vale para los trigger. 
#inspect, me vale para que dentro de cada trigger sepa el valor de old y new.  (que es algo que yo usaba con facilidad en postgres)
from sqlalchemy import event, inspect 

#time delta me vale para poner trozos de tiempo, por ejemplo, en este proyecto, he puesto trozos de 5 minutos. 
from datetime import datetime, timedelta

# estlas librerias son para hacer los rangos con GIST y tratar a robot como entidad física. 
from sqlalchemy.dialects.postgresql import ExcludeConstraint

# DDL es para poder pasar codigo posquesql directamende desde este script a postgres. 
# func me vale para hacer el rango desde inicio hasta fin. 
# el checkConstraint me vale para hacer un check al igual que lo hacia en postgres. 
# el and, me vale pare hacer expresones en sqlAlchemy, y de esta forma poder tener and en los checkConstrait. 
from sqlalchemy import event, DDL, func, CheckConstraint, and_, or_

# esto me vale para validar el campo de fecha de comienzo en evento, el cual tiene que ser mayor o igual que la fecha actual del sistema. 
# esto es para poder hacer el join: aliased, y que de esta manea pueda poner una tabla dentro del join. (inner join SQL).  
from sqlalchemy.orm import validates, aliased

from werkzeug.security import check_password_hash


# en esta lista voy a alamecenar todos los robots que no estan en servicio, para que cuando se haga la consulta de conseguir robots de un evento, me va a devolver los robots del evento, pero sin saber cual de ellos es el que está en servicio, porque 
#recoordar que esto no lo puedo guardar en la BBDD, por lo tanto en este script lo activo o desactivo y lo puede usar el script main.py para que el asistente averigue si puede manejar un robo o no. 
from estructuradatos import miListaRobotsQueNoEstanEnServicio;  
from estructuradatos import miDiccionarioEventoYasistentesDatos;  
 
db = SQLAlchemy();

class Administrador(db.Model):
    __tablename__ = "miTablaAdministrador";
    __correoElectronico = db.Column(db.String(50), primary_key=True)
    __contrasena = db.Column(db.String(162), nullable=False)
    # esto no es un atributo, si no una relación. No la voy a declarar como privada ya que para eso deberia conseguir algún valor de alguna columna, y es que esas coloumnas ya son privadas. 
    administrador_correoElectronico_relacionEvento = db.relationship("Evento", backref="administrador_correoElectronico_relacionEvento_backref", cascade="all"); #esto permite que el delete sea cascade. 

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
        
    def validarContrasena (self, password):
        miAdministrador  = Administrador.query.filter_by (_Administrador__correoElectronico= self.__correoElectronico).first ();
        miContrasenaConHash = miAdministrador.contrasena;
        if (check_password_hash(miContrasenaConHash, password)):
            return True;
        else:
            return False;
        
    def funcion_crearRobot (self, parametroMacAddressDelRobot, parametroNombreDelRobot, parametroFotoDelRobot=None, parametroDescripcionDelRobot=None):
        miRobot = Robot (macAddressDelRobot=parametroMacAddressDelRobot, nombreDelRobot=parametroNombreDelRobot, fotoDelRobot=parametroFotoDelRobot, descripcionDelRobot=parametroDescripcionDelRobot);
        db.session.add (miRobot);
        db.session.commit ();
        
        
    def funcion_modificarRobot (self, parametroIdRobot, parametroMacAddressDelRobot=None, parametroNombreDelRobot=None, parametroFotoDelRobot=None, parametroDescripcionDelRobot=None):
        #print ("funcion_modificarRobot ()---",  parametroIdRobot, "+", parametroMacAddressDelRobot);
        miRobot = Robot.query.filter_by (_Robot__idRobot = parametroIdRobot).first();
        if (miRobot == None):
            raise Exception ("exception. No se puede modificar el robot, ya que el robot que has puesto no existe en la BBDD ");
        else:
            if (parametroMacAddressDelRobot == None):
                parametroMacAddressDelRobot = miRobot.macAddressDelRobot;
            else:
                if (miRobot.macAddressDelRobot != parametroMacAddressDelRobot):  #este es para que en el caso de que un robot este siendo controlado, y justo en ese momento, se le cambiia la mac, entonces a ese asistente se le va a declarar como esProvilegiado y le expulsara del robot.
                    miListaRobotsQueNoEstanEnServicio.append (parametroIdRobot);  # cuidado,porque esto signica que en el caso de que yo cambie la MAC de un robot, significa que ese robot deja de estar en servicio. 
                    #print ("funcion_modificarRobot ()---las MAC son distintas, antigua: ", miRobot.macAddressDelRobot +" la nueva: " +parametroMacAddressDelRobot);  
                    miAsistente = Asistente.query.filter (Asistente._Asistente__robot_idRobot == parametroIdRobot, Asistente._Asistente__fechaTomaDelRobot <= datetime.now(), Asistente._Asistente__fechaAbandonoDelRobot >= datetime.now()).first (); 
                    if (miAsistente):  # en el caso de que lo encuentre, a ese lo pongo como es privilegiado. 
                        # ahora voy hacer los modificaciones en el asistenten por parte de la aplicacion, es decir en el diccionario de eventos. 
                        for indiceNumerico, i in enumerate(miDiccionarioEventoYasistentesDatos[miAsistente.evento_idEvento]):
                            if (miAsistente.tokenDeSesion == i[0]):  # recordar que en el indice 0, es donde yo guardo al token de sesion.  En este if si se cumple, es que lo he encontrado. 
                                miDiccionarioEventoYasistentesDatos[miAsistente.evento_idEvento][indiceNumerico][2] = True; # aqui he encontrado la lista, y de ella, el inidice 2 es el valor de esPrivilegiado, este lo pongo en True.  
                        miAsistente.fechaAbandonoDelRobot = datetime.now (); # aqui lo que hago es de la fecha de abandono, ponerle la fecha actual, para que de esta forma en la BBDD se vea que ese asistente ya no tiene ese robot. 
                        db.session.commit ();
                    miRobot.macAddressDelRobot = parametroMacAddressDelRobot;

            if (parametroNombreDelRobot == None):
                parametroNombreDelRobot = miRobot.nombreDelRobot;
            else:
                miRobot.nombreDelRobot = parametroNombreDelRobot;
                
            if (parametroFotoDelRobot == None):
                parametroFotoDelRobot = miRobot.fotoDelRobot;
            else:
                miRobot.fotoDelRobot = parametroFotoDelRobot;
                
            if (parametroDescripcionDelRobot== None):
                parametroDescripcionDelRobot = miRobot.descripcionDelRobot;
            else:
                miRobot.descripcionDelRobot = parametroDescripcionDelRobot;
                
            db.session.commit ();
        
    def funcion_borrarRobot (self, parametroIdRobot):
        miRobot = Robot.query.filter_by (_Robot__idRobot=parametroIdRobot).first ();
        if (miRobot == None):
            raise Exception ("exception. No se puede borrar el robot, ya que el robot que has puesto no existe en la BBDD ");
        else:
            # lo que voy a hacer aqui es modificar la clava formea de los eventos que tengan com clave foranea a ese robot que estoy apunto de borrar. 
            miListaDeEventos = Evento.query.filter_by (_Evento__administrador_correoElectronico= self.__correoElectronico).all ();
            for i in miListaDeEventos: 
                if i.robot_idRobot == parametroIdRobot: 
                    miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento == i.idEvento, DisponibleRobot.robot_idRobot != parametroIdRobot).first ();
                    if (miDisponibleRobot): # en este caso al menos he econtrado un robot, por lo tanto el evento no se borrara en cascade, debido a el borrado del robot. 
                        i.robot_idRobot = miDisponibleRobot.robot_idRobot;
                        db.session.commit ();
            db.session.delete (miRobot);
            db.session.commit();
            
    def funcion_activarOdesactivarRobot (self, parametroIdRobot, parametroEnServicio):
        #print ("funcion_activarOdesactivarRobot ()--- esta es la la lista: ");
        miRobot = Robot.query.filter_by (_Robot__idRobot=parametroIdRobot).first();
        if (miRobot):
            if (parametroEnServicio <= 0):  
                miListaRobotsQueNoEstanEnServicio.append (parametroIdRobot);
                #print ("funcion_activarOdesactivarRobot ()--- se va a meter un robot en la lsita de los que no estan en servicio ");
                # acabo de quitar del servicio a un robot, por lo tanto aqui lo que voy a hacer es ver si hay un asistente que tenga ese robot en ese momento. 
                miAsistente = Asistente.query.filter (Asistente._Asistente__robot_idRobot == parametroIdRobot, Asistente._Asistente__fechaTomaDelRobot <= datetime.now(), Asistente._Asistente__fechaAbandonoDelRobot >= datetime.now()).first (); 
                if (miAsistente):  # en el caso de que lo encuentre, a ese lo pongo como es privilegiado. 
                    # ahora voy hacer los modificaciones en el asistenten por parte de la aplicacion, es decir en el diccionario de eventos. 
                    for indiceNumerico, i in enumerate(miDiccionarioEventoYasistentesDatos[miAsistente.evento_idEvento]):
                        if (miAsistente.tokenDeSesion == i[0]):  # recordar que en el indice 0, es donde yo guardo al token de sesion.  En este if si se cumple, es que lo he encontrado. 
                            miDiccionarioEventoYasistentesDatos[miAsistente.evento_idEvento][indiceNumerico][2] = True; # aqui he encontrado la lista, y de ella, el inidice 2 es el valor de esPrivilegiado, este lo pongo en True.  
                    miAsistente.fechaAbandonoDelRobot = datetime.now (); # aqui lo que hago es de la fecha de abandono, ponerle la fecha actual, para que de esta forma en la BBDD se vea que ese asistente ya no tiene ese robot. 
                    db.session.commit ();
                    #print ("funcion_activarOdesactivarRobot ()--- en la BBDD en la tabla Asistente, se ha establecido la feha de abandono ");
            else:
                miListaRobotsQueNoEstanEnServicio.remove (parametroIdRobot);
                #print ("funcion_activarOdesactivarRobot ()--- se ha eliminado un robot de la lista de los que no estan en servicio. ");
        #print (miListaRobotsQueNoEstanEnServicio);
        
    def funcion_conseguirTodosLosRobots (self):
        return Robot.query.all();
        
    def funcion_conseguirTodosLosRobotsQueNoSonDelAdministradorDeEseEvento (self, parametroIdEvento):
        miListaEvento = Evento.query.filter (Evento._Evento__administrador_correoElectronico != self.__correoElectronico).all ();
        #print ("funcion_conseguirTodosLosRobotsQueNoSonDelAdministrador()---", miListaEvento);
        miListaRobot = [];
        for i in miListaEvento: 
            miListaDisponibleRobot = DisponibleRobot.query.filter_by (evento_idEvento=i._Evento__idEvento).all ();
            for j in miListaDisponibleRobot:
                miRobot = Robot.query.filter_by (_Robot__idRobot=j.robot_idRobot).first();
                if (miRobot not in miListaRobot):
                    miListaRobot.append (miRobot);
                    
        miConjuntoRobotsPropierarioOtrosAdministradores = set (miListaRobot);
        #print ("funcion_conseguirTodosLosRobotsQueNoSonDelAdministrador()---", miConjuntoRobotsPropierarioOtrosAdministradores);
                    
        miListaRobot = []
        miListaDisponibleRobot = DisponibleRobot.query.filter_by (evento_idEvento=parametroIdEvento).all ();
        for j in miListaDisponibleRobot:
            miRobot = Robot.query.filter_by (_Robot__idRobot=j.robot_idRobot).first();
            if (miRobot not in miListaRobot):
                miListaRobot.append (miRobot);
        
        miConjuntoRobotsPropierarioAdministrador = set (miListaRobot);
        miConjuntoRobotsQueNoSonDelAdministrador = miConjuntoRobotsPropierarioOtrosAdministradores.difference (miConjuntoRobotsPropierarioAdministrador);
        #print ("funcion_conseguirTodosLosRobotsQueNoSonDelAdministrador()---", miConjuntoRobotsPropierarioAdministrador);
        #print ("funcion_conseguirTodosLosRobotsQueNoSonDelAdministrador()---", miConjuntoRobotsQueNoSonDelAdministrador);
        
        # en esta ultima parte lo que hago es conseguir los robots que no estan en ningun evento. para que los sume a los robots que no son del administrador pero que estan en la tabla de disponibleRobot. 
        miListaRobotsQueNoEstanEnNingunEvento = self.funcion_conseguirRobotsQueNoEtanEnNingunEvento();
        for i in miListaRobotsQueNoEstanEnNingunEvento:
            miConjuntoRobotsQueNoSonDelAdministrador.add (i);
            
        
        return miConjuntoRobotsQueNoSonDelAdministrador;
        
    def funcion_conseguirRobotPorIdRobot (self, parametroIdRobot):
        return Robot.query.filter_by (_Robot__idRobot=parametroIdRobot).first();
        
    def funcion_conseguirRobotsQueNoEtanEnNingunEvento (self):
        miDisponibleRobotAlias = aliased (DisponibleRobot);
        return db.session.query(Robot).outerjoin (miDisponibleRobotAlias, Robot._Robot__idRobot == miDisponibleRobotAlias.robot_idRobot).filter (miDisponibleRobotAlias.robot_idRobot==None).all ();
        
    def funcion_verSiPuedoBorrarRobot (self, paramametroIdRobot):
        miVerdadPuedoBorrarRobot = True;
        miEventoAlias = aliased (Evento);
        miDisponibleRobot = db.session.query(DisponibleRobot).join(miEventoAlias, DisponibleRobot.evento_idEvento==miEventoAlias._Evento__idEvento).filter (DisponibleRobot.robot_idRobot==paramametroIdRobot, miEventoAlias._Evento__administrador_correoElectronico!=self.__correoElectronico).first();  
        if (miDisponibleRobot == None):
            pass; 
            #print ("funcion_verSiPuedoBorrarRobot()--- si que se puede borrar el robot, solo es de ese administrador. ");
        else:
            #print ("funcion_verSiPuedoBorrarRobot()--- no se puede borrar el robot, ese robot es de más administradores.  ");
            miVerdadPuedoBorrarRobot = False;
        return miVerdadPuedoBorrarRobot;
            
    def funcion_verSiPuedoModificarRobot (self, paramametroIdRobot):
        miVerdadPuedoModificarRobot = True;
        # en este punto veo si en el momento actual del sistema el robot esta en un evento, es decir está en la tabla de disponibleRobot. 
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robot_idRobot==paramametroIdRobot, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).first();
        if (miDisponibleRobot):  # aqhui he coprobado que es verdad que el robot en el momento actual, esta en un evento por lo tanto  dentro de este if voy a averiguar que evento es, para del evento sacar quien es el administrador. 
            miEvento = Evento.query.filter_by (_Evento__idEvento=miDisponibleRobot.evento_idEvento).first ();
             # aqui comparo el administrador dueño del evento con el administrador que ha sido instanciodo, para devolver si puedo o no modificar ese robot.  En el caso de que no sean los mismos, entonces significa que otro administrador
             # tiene en un evento actualmente ese robot, por lo tanto el administrador que ha isntaciado la clase no puede tocar sus parametros, se devolverá False. 
            if (miEvento.administrador_correoElectronico != self.__correoElectronico):
                miVerdadPuedoModificarRobot = False;
        
        return miVerdadPuedoModificarRobot;
        
##### funciones que menejan el evento  ##############################################################################################################################################

    def funcion_conseguirEventoPorIdEvento (self, parametroIdEvento):
        return Evento.query.filter_by (_Evento__idEvento=parametroIdEvento).first();
        
    def funcion_crearEvento (self, miParametroListaDisponibleRobot, parametroIdEvento, parametroNombreDelEvento, parametroCalle=None, parametroNumero=None, parametroEdificioDondeSeCelebra=None, parametroCodigoPostal=None):
        if (len (miParametroListaDisponibleRobot) == 0):
            #print ("crearEvento()---la pila esta vacia: ", miParametroListaDisponibleRobot);
            #print ("crearEvento()---No voy a crear el evento ya que no tengo ningun robot para asociar ese evento a un robot. ");
            raise Exception ("exception. No se puede crear el evento, ya que no ha asignado ningún robot a este (recordar evento necesita al menos un robot)");
        else:
            #print ("crearEvento()--- la pila tiene eementos, aqui estan: ");
            #print (miParametroListaDisponibleRobot);
            #print ("crearEvento()--- esta es la cima:  ", miParametroListaDisponibleRobot[-1]);
            # en este evento que acabo de crear 
            miEvento = Evento (idEvento=parametroIdEvento, nombreDelEvento=parametroNombreDelEvento, calle=parametroCalle, fechaDeCreacionDelEvento=datetime.now(), numero=parametroNumero, edificioDondeSeCelebra=parametroEdificioDondeSeCelebra, 
            codigoPostal=parametroCodigoPostal, administrador_correoElectronico=self.__correoElectronico, robot_idRobot=miParametroListaDisponibleRobot[-1][1]);
            #print ("crearEvento()--- ", parametroEdificioDondeSeCelebra);
            db.session.add (miEvento);
            
            for miDisponibleRobotValores in miParametroListaDisponibleRobot:
                #print ("crearEvento()---");
                miDisponibleRobot = DisponibleRobot (evento_idEvento=miDisponibleRobotValores[0],robot_idRobot=miDisponibleRobotValores[1], fechaComienzoEnEvento=miDisponibleRobotValores[2], fechaFinEnEvento=miDisponibleRobotValores[3]);
                db.session.add (miDisponibleRobot);
                db.session.commit ();
            miParametroListaDisponibleRobot.clear();
            #print (miParametroListaDisponibleRobot);
        
    def funcion_conseguirTodosLosEventos (self):
        return Evento.query.all();
        
    def funcion_conseguirTodosLosEventosDeEseAdministrador (self):
        return Evento.query.filter_by (_Evento__administrador_correoElectronico=self.correoElectronico).all();
        
    def funcion_conseguirTodosLosEventosPorCorreoElectronico (self, parametroCorreoElectronico):
        return Evento.query.filter_by (_Evento__administrador_correoElectronico = parametroCorreoElectronico).all();
        
    def funcion_conseguirDisponibleRobotPorEvento (self, miParametroIdEvento):
        return DisponibleRobot.query.filter_by (evento_idEvento=miParametroIdEvento).all();
        
        
    def funcion_modificarDatosDelEvento (self, parametroAntiguoIdEvento, parametroNuevoIdEveto, parametroNombreDelEvento, parametroCalle=None, parametroNumero=None, parametroEdificioDondeSeCelebra=None, parametroCodigoPostal=None):
        print ("modificarDatosDelEvento()---", parametroAntiguoIdEvento);
        
        miEvento = Evento.query.filter_by (_Evento__idEvento=parametroAntiguoIdEvento).first ();
        if (miEvento == None):
            raise Exception ("exception. No se puede modificar el evento ya que ese evento no existe");
        else:
            if (self.__correoElectronico != miEvento.administrador_correoElectronico):
                raise Exception ("exception. No se puede modificar los datos del evento, ese administrador no es el dueño del evento ");
            else:
                miEvento.idEvento = parametroNuevoIdEveto;
                miEvento.nombreDelEvento = parametroNombreDelEvento;
                if (parametroCalle != None):
                    miEvento.calle = parametroCalle;
                if (parametroNumero != None):
                    miEvento.numero = parametroNumero;
                if (parametroEdificioDondeSeCelebra != None):
                    miEvento.edificioDondeSeCelebra = parametroEdificioDondeSeCelebra;
                if (parametroCodigoPostal != None):
                    miEvento.codigoPostal = parametroCodigoPostal;
                db.session.commit ();
                
    # esta la dejo junto con las funciones que manejan el evento, ya que lo que se esta modificando es el evento debido a que un robot es una parte del evento. 
    def funcion_modificarRobotDelEvento (self, parametroEvento_idEvento, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento, parametroNuevaFechaComienzoEnEvento, parametroNuevaFechaFinEnEvento):
        #print ("funcion_modificarRobotDelEvento()---");
        #print ("funcion_modificarRobotDelEvento()---", parametroEvento_idEvento);
        #print ("funcion_modificarRobotDelEvento()---", parametroRobot_idRobot);
        #print ("funcion_modificarRobotDelEvento()---", parametroFechaComienzoEnEvento);
        #print ("funcion_modificarRobotDelEvento()---", parametroFechaFinEnEvento);
        
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento==parametroEvento_idEvento, DisponibleRobot.robot_idRobot==parametroRobot_idRobot, DisponibleRobot.fechaComienzoEnEvento==parametroFechaComienzoEnEvento,DisponibleRobot.fechaFinEnEvento==parametroFechaFinEnEvento).first();
        if (miDisponibleRobot == None):
            raise Exception ("exception. No se puede modificar el horario de ese robot, ese horario no existe. ");
        else:
            #print ("modificarRobotsDelEvento()--- si se va a modificar DisponibleRobot. ");
            miDisponibleRobot.fechaComienzoEnEvento = parametroNuevaFechaComienzoEnEvento;
            miDisponibleRobot.fechaFinEnEvento = parametroNuevaFechaFinEnEvento;
            db.session.commit ();
    
    # esta la dejo junto con las funciones que manejan el evento, ya que lo que se esta modificando es el evento debido a que un robot es una parte del evento. 
    def funcion_sumarRobotAlEvento (self, parametroEvento_idEvento, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento):
        miDisponibleRobot = DisponibleRobot (evento_idEvento=parametroEvento_idEvento, robot_idRobot=parametroRobot_idRobot, fechaComienzoEnEvento=parametroFechaComienzoEnEvento, fechaFinEnEvento=parametroFechaFinEnEvento);
        db.session.add (miDisponibleRobot);
        db.session.commit ();
    
    def funcion_eliminarRobotDelEvento (self, parametroEvento_idEvento, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento):
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento == parametroEvento_idEvento, DisponibleRobot.robot_idRobot == parametroRobot_idRobot, DisponibleRobot.fechaComienzoEnEvento == parametroFechaComienzoEnEvento, DisponibleRobot.fechaFinEnEvento == parametroFechaFinEnEvento).first ();
        db.session.delete (miDisponibleRobot);
        db.session.commit ();
        
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento==parametroEvento_idEvento, DisponibleRobot.robot_idRobot==parametroRobot_idRobot).first ();
        if (miDisponibleRobot == None):
            #print ("funcion_eliminarRobotDelEvento()--- ese horario ha sido el ultimo asociado al robot, se va a cambair la clave foranea en Evento o se va a eliminar el robot. ");
            miDisponibleRobot = DisponibleRobot.query.filter_by (evento_idEvento=parametroEvento_idEvento).first ();
            miEvento = Evento.query.filter_by (_Evento__idEvento = parametroEvento_idEvento).first ();  #lo dejo aqui, porque aqui ya se que o se borra o se modifica la clave foranea. 
            if (miDisponibleRobot == None): 
                #print ("funcion_eliminarRobotDelEvento()--- ya que no el robot no esta asociado a ningun evento, lo que voy a hacer va ser eliminarlo. ");
                db.session.delete (miEvento);
                db.session.commit ();
            else:   # aqui lo que hago es actuliza la clave foranea hacia la entidad Robot para que esta sea un robot de la tabla de disponible, no es necesario, pero da sentido a la BBDD. 
                #print ("funcion_eliminarRobotDelEvento()--- ese horario ha sido el ultimo asociado al robot, se va a cambair la clave foranea en Evento");
                miEvento.robot_idRobot = miDisponibleRobot.robot_idRobot;
                db.session.commit ();
                    
    def funcion_borrarEvento (self, parametroIdEvento):
        miEvento = Evento.query.filter_by (_Evento__idEvento=parametroIdEvento).first ();
        if (miEvento == None):
            raise Exception ("exception. No se puede borrar el evento, ya que no existe en la BBDD.");
        else:
            if (miEvento.administrador_correoElectronico != self.__correoElectronico):
                raise Exception ("exception. No se puede borrar el evento, ya que ese administrador no es el dueño");
            else:
                db.session.delete (miEvento);
                db.session.commit ();
                
    def funcion_borrarRobotDelEvento (self, parametroEvento_idEvento, parametroRobot_idRobot, parametroFechaComienzoEnEvento, parametroFechaFinEnEvento):
        #print ("funcion_borrarRobotDelEvento()--- ");
        
        miEvento = Evento.query.filter_by (_Evento__idEvento = parametroEvento_idEvento).first();
        if (miEvento.administrador_correoElectronico != self.__correoElectronico):
            raise Exception ("exception. No se puede borrar el horario de ese robot, ese administrador no es el dueño del evento");
        else:
            miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento==parametroEvento_idEvento, DisponibleRobot.robot_idRobot==parametroRobot_idRobot, DisponibleRobot.fechaComienzoEnEvento==parametroFechaComienzoEnEvento, 
            DisponibleRobot.fechaFinEnEvento==parametroFechaFinEnEvento).first();
            if (miDisponibleRobot == None):
                raise Exception ("exception. No se puede borrar el horario de ese robot, ese horario no existe");
            else:
                db.session.delete (miDisponibleRobot);
                db.session.commit ();
                
    def funcion_verSiEseEventoTieneAlMenosUnRobot (self, parametroIdEvento):
        #print ("funcion_verSiEseEventoTieneAlMenosUnRobot() --- ");
        miVerdadVerSiHayMasEventos = True; 
        miDisponibleRobot = DisponibleRobot.query.filter_by (evento_idEvento= parametroIdEvento).first ();
        if (miDisponibleRobot == None):
            miVerdadVerSiHayMasEventos = False;
        #print ("funcion_verSiEseEventoTieneAlMenosUnRobot() --- ", miVerdadVerSiHayMasEventos);
        return miVerdadVerSiHayMasEventos;
        
##### funciones que menejan las cuentas de los administradores  ##############################################################################################################################################

    def funcion_conseguirTodasLasCuentasMenosLaInstanciada (self):
        #print ("funcion_conseguirTodasLasCuentasMenosLaInstanciada()---");
        return Administrador.query.filter (Administrador._Administrador__correoElectronico != self.__correoElectronico).all ();
        
    def funcion_borrarCuaentaAdministrador (self, parametroCorreoElectronico):
        #print ("funcion_borrarCuaentaAdministrador()----");
        miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico = parametroCorreoElectronico).first ();
        db.session.delete (miAdministrador);
        db.session.commit ();
        

# esto me vale para que el indice gist funcione con enteros. 
sqlParaPoderUtilizarGistConEnteros = """CREATE EXTENSION IF NOT EXISTS btree_gist;"""
event.listen (Administrador.__table__, 'before_create', DDL(sqlParaPoderUtilizarGistConEnteros));

class Robot (db.Model):
    __tablename__ = "miTablaRobot";
    __idRobot = db.Column (db.Integer, primary_key = True);
    __macAddressDelRobot = db.Column (db.String (12), unique=True, nullable = False); 
    __nombreDelRobot = db.Column (db.String (50), unique=True, nullable = False);
    __fotoDelRobot = db.Column (db.LargeBinary); 
    __descripcionDelRobot = db.Column (db.String (100));
    robot_idRobot_relacionEvento = db.relationship("Evento", backref="robot_idRobot_relacionEvento_backref", cascade="all"); 
    robot_idRobot_relacionDisponibleRobot = db.relationship ("DisponibleRobot", backref="robot_idRobot_relacionDisponibleRobot_backref", cascade="all");
    robot_idRobot_relacionAsistente = db.relationship("Asistente", backref="robot_idRobot_relacionAsistente_backref", cascade="all"); 

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

class Evento(db.Model):   
    __tablename__ = "miTablaEvento";
    __idEvento = db.Column (db.Integer, primary_key = True);
    __nombreDelEvento = db.Column (db.String (50), nullable=False, unique=True);
    __fechaDeCreacionDelEvento = db.Column (db.DateTime, nullable=False);
    __calle = db.Column (db.String (50));
    __numero = db.Column (db.String (50));
    __edificioDondeSeCelebra = db.Column (db.String (50));
    __codigoPostal = db.Column (db.Integer);
    __administrador_correoElectronico = db.Column (db.String (50), db.ForeignKey ('miTablaAdministrador._Administrador__correoElectronico', onupdate="CASCADE"), nullable=False); # esto permite que el update sea cascade. 
    __robot_idRobot = db.Column (db.Integer, db.ForeignKey ('miTablaRobot._Robot__idRobot', onupdate="CASCADE"), nullable=False);
    evento_idEvento_relacionDisponibleRobot = db.relationship("DisponibleRobot", backref="evento_idEvento_relacionDisponibleRobot_backref", cascade="all");
    evento_idEvento_relacionAsistente = db.relationship("Asistente", backref="evento_idEvento_relacionAsistente_backref", cascade="all");

    @property
    def idEvento (self):
        return self.__idEvento;
    @idEvento.setter
    def idEvento (self, value):
        self.__idEvento = value;
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
    def edificioDondeSeCelebra (self):
        return self.__edificioDondeSeCelebra;
    @edificioDondeSeCelebra.setter
    def edificioDondeSeCelebra (self, value):
        self.__edificioDondeSeCelebra = value;

    @property
    def codigoPostal (self):
        return self.__codigoPostal;
    @codigoPostal.setter
    def codigoPostal (self, value):
        self.__codigoPostal = value;
    @property
    def administrador_correoElectronico (self):
        return self.__administrador_correoElectronico;
    @administrador_correoElectronico.setter
    def administrador_correoElectronico (self, value):
        self.__administrador_correoElectronico = value;
    @property
    def robot_idRobot (self):
        return self.__robot_idRobot;
    @robot_idRobot.setter
    def robot_idRobot (self, value):
        self.__robot_idRobot = value;

class Asistente (db.Model):
    __tablename__ = "miTablaAsistente";
    __idAsistente = db.Column (db.Integer, primary_key = True);
    __tokenDeSesion = db.Column (db.String (48), nullable = False);
    __fechaTomaDelRobot = db.Column (db.DateTime, nullable=False);
    __fechaAbandonoDelRobot = db.Column (db.DateTime, nullable=False);
    __evento_idEvento = db.Column (db.Integer, db.ForeignKey ('miTablaEvento._Evento__idEvento', onupdate="CASCADE"), nullable=False);
    __robot_idRobot = db.Column (db.Integer, db.ForeignKey ('miTablaRobot._Robot__idRobot', onupdate="CASCADE"), nullable=False);
    
    #REQUSITO7. #REQUISITO8. 
    __table_args__ = (ExcludeConstraint((__robot_idRobot, '='),(func.tstzrange(func.timezone('UTC', __fechaTomaDelRobot), func.timezone('UTC', __fechaAbandonoDelRobot)), '&&'), name='miExclusionFechasYrobot_idRobotTablaAsistente', using='gist'), 
    ExcludeConstraint((__tokenDeSesion, '='),(func.tstzrange(func.timezone('UTC', __fechaTomaDelRobot), func.timezone('UTC', __fechaAbandonoDelRobot)), '&&'), name='miExclusionFechasYasistente_tokenDeSesionTablaAsiste', using='gist'), );
    
    @property
    def idAsistente (self):
        return self.__idAsistente;
    @idAsistente.setter 
    def idAsistente (self, value):
        self.__idAsistente = value;
    
    @property
    def tokenDeSesion (self):
        return self.__tokenDeSesion;
    @tokenDeSesion.setter 
    def tokenDeSesion (self, value):
        self.__tokenDeSesion = value;
        
    @property
    def fechaTomaDelRobot (self):
        return self.__fechaTomaDelRobot;
    @fechaTomaDelRobot.setter 
    def fechaTomaDelRobot (self, value):
        self.__fechaTomaDelRobot = value;
        
    @property
    def fechaAbandonoDelRobot (self):
        return self.__fechaAbandonoDelRobot;
    @fechaAbandonoDelRobot.setter 
    def fechaAbandonoDelRobot (self, value):
        self.__fechaAbandonoDelRobot = value;
        
    @property
    def robot_idRobot (self):
        return self.__robot_idRobot;
    @robot_idRobot.setter
    def robot_idRobot (self, value):
        self.__robot_idRobot = value;

    @property
    def evento_idEvento (self):
        return self.__evento_idEvento;
    @evento_idEvento.setter
    def evento_idEvento (self, value):
        self.__evento_idEvento = value;
        

    def funcion_consultaEvento (self, parametroIdEvento):
        return Evento.query.filter_by (_Evento__idEvento=parametroIdEvento).first ();
        
    def funcion_consultaRobot (self, parametroIdRobot):
        return Robot.query.filter_by (_Robot__idRobot=parametroIdRobot).first();

class DisponibleRobot (db.Model):
    __tablename__ = "miTablaDisponibleRobot";
    idDisponibleRobot = db.Column(db.Integer, primary_key=True);
    robot_idRobot = db.Column(db.Integer, db.ForeignKey('miTablaRobot._Robot__idRobot', onupdate="CASCADE"), nullable=False);
    evento_idEvento = db.Column(db.Integer, db.ForeignKey('miTablaEvento._Evento__idEvento', onupdate="CASCADE"), nullable=False);
    fechaComienzoEnEvento = db.Column(db.DateTime, nullable=False);
    fechaFinEnEvento = db.Column(db.DateTime, nullable=False);


    #REQUSITO4. 
    __table_args__ = (ExcludeConstraint((robot_idRobot, '='),(func.tstzrange(func.timezone('UTC', fechaComienzoEnEvento), func.timezone('UTC', fechaFinEnEvento)), '&&'), name='miExclusionFechasYrobot_idRobotTablaDisponibleRobot', using='gist'),);



###TRIGGER################################################################################################################################################################################################

#REQUSITO9. 
@event.listens_for (Asistente, 'before_insert')
def trigger_funcion_B_I_antesDeManejarRobotRevisarRequisitos (mapper, connection, target):
    miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robot_idRobot==target.robot_idRobot, DisponibleRobot.evento_idEvento==target.evento_idEvento, DisponibleRobot.fechaComienzoEnEvento<=datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).first();
    if (miDisponibleRobot == None):
        raise Exception ("exception.B_I. Ese robot no esta en el evento.");
    else:
        miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robot_idRobot==target.robot_idRobot, DisponibleRobot.evento_idEvento==target.evento_idEvento, DisponibleRobot.fechaComienzoEnEvento<=target.fechaTomaDelRobot, DisponibleRobot.fechaFinEnEvento >= target.fechaAbandonoDelRobot).first();
        if (miDisponibleRobot == None):
            raise Exception ("exception.B_I. Ese robot sí esta en el evento, pero la fecha de manejo establecida con el asistente, no esta comprendida entre la de comienzo y fin en el evento con el roobot.");


    
    




