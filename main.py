# el request,  me vale para recibir parámetros por a URL. 
# el redirect me vale para redirigir a los usuarios a otra pagina de mi aplicacion. 
# el url_for genera una url para una de las funciones que tengo en este main.py. 
from flask import Flask, request, render_template, redirect, url_for, session

from models import db
from config import DevelopmentConfig  #Desde mi archivo config.py importo esta clase. 

from models import Administrador, Robot, Evento, Asistente, DisponibleRobot

from datetime import datetime, timedelta 

import formulario

from flask import send_file  #esto es para que el HTML pida la foto y con esto se la envie. 
from io import BytesIO  # esto lo que hace es convertir la lista da bits de la foto en algo entendible para el navegador. 

import os # esto es para sacar valores random del sistema operativo, lo uso para crear mi propio token para los aistentes.

#from werkzeug.security import generate_password_hash # si quiero usar esto, tengo que hacer:  pip install Werkzeug
from werkzeug.security import generate_password_hash 

# esta libreria es para poder enviar JSON al cliente. 
from flask import jsonify

# esto me vale para utilizar expresiones regulares en pyrhon. 
import re

app = Flask(__name__)
app.config.from_object (DevelopmentConfig);

from estructuradatos import miListaRobotsQueNoEstanEnServicio;
from estructuradatos import miDiccionarioEventoYasistentesDatos;

# en este diccionario la clave va a ser el token con el evento , para saber que asistenten en que evento hay rechazado un robot, para que de esta forma no se le muestre uno que el haya rechazado en el evento. 
miDiccionarioGlobalTokensListaDeRobotsRechazados = {}

# este diccionario me va a valer para ponerlo en el before request, para que solamente cada minuto se pueda pasar a esPrivilegiado a los asistentes debido a inactividad. 
miDiccionarioFechasPasoAEsPrivilegiado = {}

@app.route ("/index")
def index ():
    return "<p>Hello, World! Demostraciones Robóticas.</p>"
    

@app.route ("/index2")
def index2 ():
    contrasnaHasheda = generate_password_hash ("james")
    miAdmin1 = Administrador (correoElectronico="jhon@gmail.com", contrasena=contrasnaHasheda);
    miAdmin2 = Administrador (correoElectronico="ana@gmail.com", contrasena=contrasnaHasheda);
    miAdmin3 = Administrador (correoElectronico="alberto@gmail.com", contrasena=contrasnaHasheda);
    db.session.add (miAdmin1);
    db.session.add (miAdmin2);
    db.session.add (miAdmin3);
    db.session.commit();

    robot1 = Robot(idRobot=101, macAddressDelRobot="AA:BB:CC:DD:EE:FF", nombreDelRobot="Robot Explorador1");
    robot2 = Robot(idRobot=102, macAddressDelRobot="AA:BB:CC:DD:EE:00", nombreDelRobot="Robot Explorador2");
    robot3 = Robot(idRobot=103, macAddressDelRobot="AA:BB:CC:DD:EE:11", nombreDelRobot="Robot Explorador3");
    robot4 = Robot(idRobot=104, macAddressDelRobot="AA:BB:CC:DD:EE:22", nombreDelRobot="Robot Explorador4");
    robot5 = Robot(idRobot=105, macAddressDelRobot="AA:BB:CC:DD:EE:33", nombreDelRobot="Robot Explorador6");
    robot6 = Robot(idRobot=106, macAddressDelRobot="AA:BB:CC:DD:EE:44", nombreDelRobot="Robot Explorador7");
    robot7 = Robot(idRobot=130, macAddressDelRobot="AA:BB:CC:DD:EE:55", nombreDelRobot="Robot Explorador8");
    robot8 = Robot(idRobot=131, macAddressDelRobot="AA:BB:CC:DD:EE:66", nombreDelRobot="Robot Explorador9");
    robot9 = Robot(idRobot=132, macAddressDelRobot="AA:BB:CC:DD:EE:77", nombreDelRobot="Robot Explorador10");
    robot10 = Robot(idRobot=107, macAddressDelRobot="AA:BB:CC:DD:EE:88", nombreDelRobot="Robot Explorador11");
    robot11 = Robot(idRobot=110, macAddressDelRobot="AA:BB:CC:DD:EE:99", nombreDelRobot="Robot Explorador12");
    robot12 = Robot(idRobot=111, macAddressDelRobot="AA:BB:CC:DD:EE:AA", nombreDelRobot="Robot Explorador13");
    db.session.add (robot1);
    db.session.add (robot2);
    db.session.add (robot3);
    db.session.add (robot4);
    db.session.add (robot5);
    db.session.add (robot6);
    db.session.add (robot7);
    db.session.add (robot8);
    db.session.add (robot9);
    db.session.add (robot10);
    db.session.add (robot11);
    db.session.add (robot12);
    db.session.commit ();
    
    # cuidado porque el admininistrador es el que inserta en evento, por lo tanto, tengo que crearle a él una función para que inserte con un robot. 
    miRobot = Robot.query.filter_by ().first();
    evento1 = Evento (idEvento=1, nombreDelEvento="aula2024", fechaDeCreacionDelEvento = datetime.now(), administrador_correoElectronico = "jhon@gmail.com", robot_idRobot= miRobot.idRobot);
    evento2 = Evento (idEvento=2, nombreDelEvento="puertas abiertas2024", fechaDeCreacionDelEvento = datetime.now(), administrador_correoElectronico = "jhon@gmail.com", robot_idRobot= miRobot.idRobot);
    evento3 = Evento (idEvento=3, nombreDelEvento="mobileWeek2024", fechaDeCreacionDelEvento = datetime.now(), administrador_correoElectronico = "ana@gmail.com", robot_idRobot= robot7.idRobot);
    db.session.add (evento1);
    db.session.add (evento2);
    db.session.add (evento3);
    db.session.commit ();
    
    disponbleRobot1 = DisponibleRobot (robot_idRobot=101, evento_idEvento = 1, fechaComienzoEnEvento='2024-10-01', fechaFinEnEvento='2024-10-30');
    disponbleRobot2 = DisponibleRobot (robot_idRobot=102, evento_idEvento = 2, fechaComienzoEnEvento='2024-10-01', fechaFinEnEvento='2024-10-30');
    disponbleRobot3 = DisponibleRobot (robot_idRobot=103, evento_idEvento = 2, fechaComienzoEnEvento='2024-10-01', fechaFinEnEvento='2024-10-30');
    
    disponbleRobot4 = DisponibleRobot (robot_idRobot=101, evento_idEvento = 1, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');
    disponbleRobot5 = DisponibleRobot (robot_idRobot=103, evento_idEvento = 1, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');
    disponbleRobot6 = DisponibleRobot (robot_idRobot=105, evento_idEvento = 3, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');
    
    disponbleRobot7 = DisponibleRobot (robot_idRobot=105, evento_idEvento = 1, fechaComienzoEnEvento='2024-12-01', fechaFinEnEvento='2024-12-30');
    disponbleRobot8 = DisponibleRobot (robot_idRobot=106, evento_idEvento = 1, fechaComienzoEnEvento='2024-10-01', fechaFinEnEvento='2024-10-30');
    disponbleRobot9 = DisponibleRobot (robot_idRobot=101, evento_idEvento = 2, fechaComienzoEnEvento='2024-12-01', fechaFinEnEvento='2024-12-30');
    
    disponbleRobot10 = DisponibleRobot (robot_idRobot=107, evento_idEvento = 1, fechaComienzoEnEvento='2024-10-01', fechaFinEnEvento='2024-10-30');
    disponbleRobot11 = DisponibleRobot (robot_idRobot=101, evento_idEvento = 1, fechaComienzoEnEvento='2025-1-01', fechaFinEnEvento='2025-1-30');
    disponbleRobot12 = DisponibleRobot (robot_idRobot=130, evento_idEvento = 3, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');
    
    disponbleRobot13 = DisponibleRobot (robot_idRobot=131, evento_idEvento = 3, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');
    disponbleRobot14 = DisponibleRobot (robot_idRobot=132, evento_idEvento = 3, fechaComienzoEnEvento='2024-10-01', fechaFinEnEvento='2024-10-30');
    disponbleRobot15 = DisponibleRobot (robot_idRobot=132, evento_idEvento = 1, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');

    disponbleRobot16 = DisponibleRobot (robot_idRobot=101, evento_idEvento = 1, fechaComienzoEnEvento='2024-9-01', fechaFinEnEvento='2024-9-30');
    disponbleRobot17 = DisponibleRobot (robot_idRobot=106, evento_idEvento = 3, fechaComienzoEnEvento='2024-11-01', fechaFinEnEvento='2024-11-30');
    
    db.session.add (disponbleRobot1);
    db.session.add (disponbleRobot2);
    db.session.add (disponbleRobot3);
    db.session.add (disponbleRobot4);
    db.session.add (disponbleRobot5);
    db.session.add (disponbleRobot6);
    db.session.add (disponbleRobot7);
    db.session.add (disponbleRobot8);
    db.session.add (disponbleRobot9);
    db.session.add (disponbleRobot10);
    db.session.add (disponbleRobot11);
    db.session.add (disponbleRobot12);
    db.session.add (disponbleRobot13);
    db.session.add (disponbleRobot14);
    db.session.add (disponbleRobot15);
    db.session.add (disponbleRobot16);
    db.session.add (disponbleRobot17);

    db.session.commit ();
    
    asistente1 = Asistente (tokenDeSesion="aaa", fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now()+timedelta(minutes=5), evento_idEvento=2, robot_idRobot = 102);
    asistente2 = Asistente (tokenDeSesion="bbb", fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now()+timedelta(minutes=5), evento_idEvento=1, robot_idRobot = 101);
    asistente3 = Asistente (tokenDeSesion="ccc", fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now()+timedelta(minutes=5), evento_idEvento=2, robot_idRobot = 103);
    db.session.add (asistente1);
    db.session.add (asistente2);
    db.session.add (asistente3);
    db.session.commit ();

    return "<p>Hello, World! Demostraciones Robóticas.2 </p>"
    

@app.before_request
def miFuncionAntesDeLaPeticion ():
    #print  ("miFuncionAntesDeLaPeticion() --- este es el endpoint: ", request.endpoint); 
    miVariablePermitirAccesoSinCorreoElectronico = True;
    if (request.endpoint == 'index2') or (request.endpoint == 'funcionAdministradorsignup') or (request.endpoint == 'funcion_aceptarRobot') or (request.endpoint == 'funcion_rechazarRobot') or (request.endpoint == 'funcion_registrarAsistente') or (request.endpoint == 'static') or (request.endpoint == 'funcionAdministradorLogin'):
        miVariablePermitirAccesoSinCorreoElectronico = False
    
    # en el caso de que el correoElectronico no este en la sesion y ademas la URL que yo he puesto no sea de las permitidas, me voy al loggin. 
    if ('correoElectronico' not in session) and (miVariablePermitirAccesoSinCorreoElectronico == True):
        #print ("miFuncionAntesDeLaPeticion() --- en la sesion no esta el correo electronico, y el endpoint no es uno permitido, se va a redirigir al login. ");
        if (request.endpoint != 'funcionAdministradorLogin'):
            #print ("miFuncionAntesDeLaPeticion() --- el endpoint es el login o el sign up, finalmente no redirijo. ");
            return redirect (url_for ('funcionAdministradorLogin'));


    #print("miFuncionAntesDeLaPeticion() --- request.view_args", request.view_args);
     # en caso de que el argumento del request  sea (entre otros) el idEvento, entonces en ese evento, voy a verificar el primero de la cola. Y lo que voy a ver es si su posicionDeColaConFecha tien na antiguedad mayor a 3 minuto, y si esto es cierto
     # lo que hago es que a ese primero lo pongo como privilegiado, pero claro viendo si ha pasado como minimo un minutos de que ya se haya pasad como privilegiado a otro asistente de ese mismo evento. 
    if (request.view_args != None):  
        if (request.view_args.get('idEvento') != None):
            idEvento = request.view_args.get('idEvento');
            if (idEvento not in miDiccionarioEventoYasistentesDatos):
                miDiccionarioEventoYasistentesDatos[idEvento] = []; 
            if (idEvento not in miDiccionarioFechasPasoAEsPrivilegiado):  # en este caso que lo voy a inicializar, significa que  en ese evento un asistente no ha sido pasado por tiempo en ese evento.  (claramente).
                miDiccionarioFechasPasoAEsPrivilegiado[idEvento] = datetime.now();  
            else:
                if (datetime.now() - miDiccionarioFechasPasoAEsPrivilegiado[idEvento] >= timedelta(minutes=1)):  # de esta manera me aseguro que como maximo se va a pasar un asistente a la cola de privilegiados cada minuto, de esta manera no los meto a todos de golpe en esta nueva cola. 
                    #print  ("miFuncionAntesDeLaPeticion() --- desde que se ha pasado un asistente a la cola de privilegiado hasta la fecha actual del sistema,  ha sido  más de un minuto");
                    if (len (miDiccionarioEventoYasistentesDatos[idEvento]) > 0):  #en el caso de que tenga al menos un asistente ya en el evento. 
                        miVariableFechaMasAntigua = datetime.now ();
                        miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = None;
                        for indiceNumerico, i in enumerate (miDiccionarioEventoYasistentesDatos[idEvento]):
                            if (i[1] != None): # esto es para no tener en cuenta a las personas  que no tienen posicionDeColaConFecha, es decir cuento solamente con las que tienen fecha. Las que estan controlando un robot, o son privilegiadas no las cuento. 
                                if (i[1] < miVariableFechaMasAntigua):
                                    miVariableFechaMasAntigua = i[1];
                                    miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = indiceNumerico; # de esta manrera ya se en que posicion es donde tengo la fecha mas antigua. 
                
                        # en caso de que la fecha actual menos el elemento de la matriz, con la posicionDeColaConFecha mas antiguo, la diferncia se mayor a 3 minutos. ademas miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo tiene que haber tomado un valor. 
                        if (datetime.now () - miVariableFechaMasAntigua >= timedelta (minutes = 3)) and (miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo != None):    
                            miDiccionarioEventoYasistentesDatos[idEvento][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][1] = None; 
                            miDiccionarioEventoYasistentesDatos[idEvento][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][2] = True; 
                            miDiccionarioFechasPasoAEsPrivilegiado[idEvento] = datetime.now ();  # aqui todo la referencia del tiempo en el momento que he pasado un asistente a esPrivilegiado. 
    
    #este codigo es para que en el panel del home de cualquier administrador, se 
    if (request.endpoint == 'funcionAdministradorHome'):
        for clave, valor in miDiccionarioEventoYasistentesDatos.items():
            if (clave not in miDiccionarioFechasPasoAEsPrivilegiado): 
                miDiccionarioFechasPasoAEsPrivilegiado[clave] = datetime.now();
            else:
                if (datetime.now() - miDiccionarioFechasPasoAEsPrivilegiado[clave] >= timedelta(minutes=1)): 
                    if (len (miDiccionarioEventoYasistentesDatos[clave]) > 0):  #en el caso de que tenga al menos un asistente ya en el evento. 
                        miVariableFechaMasAntigua = datetime.now ();
                        miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = None;
                        for indiceNumerico, i in enumerate (miDiccionarioEventoYasistentesDatos[clave]):
                            if (i[1] != None): # esto es para no tener en cuenta a las personas  que no tienen posicionDeColaConFecha, es decir cuento solamente con las que tienen fecha. Las que estan controlando un robot, o son privilegiadas no las cuento.
                                if (i[1] < miVariableFechaMasAntigua):
                                    miVariableFechaMasAntigua = i[1];
                                    miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = indiceNumerico; # de esta manrera ya se en que posicion es donde tengo la fecha mas antigua. 
                        if (datetime.now () - miVariableFechaMasAntigua >= timedelta (minutes = 3)) and (miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo != None):
                            miDiccionarioEventoYasistentesDatos[clave][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][1] = None; 
                            miDiccionarioEventoYasistentesDatos[clave][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][2] = True; 
                            miDiccionarioFechasPasoAEsPrivilegiado[clave] = datetime.now ();

@app.errorhandler (404)  # esto es para sacar el HTML que contiene el mensaje de error, para los casos en los que 
# la aplicacion caiga en algun error. 
def miPaginaNoEncntradaError (e):
	return render_template ("404.html"), 404; 

# este endpoint es necesario para la representacion de las imagenes en el HTML. Ya en la base dde datos la imagen
#se alamecena codificada, lo que hago aqui es decodificarla y darsela al HTML 
@app.route ('/capturarimagenrobot/<int:idRobot>')
def funcionCapturarImagenRobot (idRobot):
    miRobot = Robot.query.filter_by (_Robot__idRobot=idRobot).first();
    #print ("funcionCapturarImagenRobot()--- ese es el robot:", miRobot);
    return send_file (BytesIO(miRobot.fotoDelRobot), mimetype='image/jpeg');
    
######## endpoints Asistente. ############################################################################################################################################################################################################
@app.route ("/<int:idEvento>") 
def funcion_registrarAsistente (idEvento):
    miEvento = Evento.query.filter_by (_Evento__idEvento = idEvento).first();
    if (miEvento == None):
        return "<p> funcion_registrarAsistente () --- error, el evento que se ha pasado por parametro, no existe. </p>";
    else:
        if (('token' in session) == False):
            session['token'] = os.urandom(24).hex(); 
            
        #aqui averiguo si ese token ya existe en el diccionario miDiccionarioEventoYasistentesDatos, para que de esta manera, no lo vuelva a meter.  
        miFilaDeDatosAsistente = [session['token'], datetime.now(), False];
        miMatrizComprobarAsistenteRegistrado = miDiccionarioEventoYasistentesDatos[idEvento];
        #print ("funcion_registrarAsistente() ---", miMatrizComprobarAsistenteRegistrado);
        miVerdadComprobarAsistenteRegistrado = False;
        for miAsistenteDatos in miMatrizComprobarAsistenteRegistrado:
            if session['token'] == miAsistenteDatos[0]:  # en el caso de quel asistente ya este registrado, lo que hago es quedarme con sus datos, no lo vuelvo a meter en el diccionario, por tanto por el lado del codigo un asistente puede estar unicamente 1 vez en un evento.
                # en este punto yo ya sé que he contrado el asistente en la matriz, tengo que hacer ademas si ese asistente ya ha usado un robot, es decir, se le ha borrado la posicionDeColaConFecha, por lo tanto en el caso de que la tenga en NULL, lo que hago 
                # es establecerle la fecha actual.  Cuidado porque para que se le ponga la fecha, tiene que pasr ademas que ese asistente no sea privilegiado. 
                if (miAsistenteDatos[1] == None) and (miAsistenteDatos[2] == False): # en el caso de que la posicionDeColaConFeha sea NULL y no sea privilegiado, le vuelvo a establecer otra posicionDeColaConFecha. 
                    miAsistenteDatos[1] = datetime.now();
                miFilaDeDatosAsistente = miAsistenteDatos;
                miVerdadComprobarAsistenteRegistrado = True;
                break;
        if (miVerdadComprobarAsistenteRegistrado == False):  # en el caso de que el asistenten no este en la matriz anterior del buble for, lo que hago es meterlo en el diccionario. 
            miDiccionarioEventoYasistentesDatos[idEvento].append(miFilaDeDatosAsistente);
                
        # ahora lo que voy a hacer es ver cuantos robots a ese asistenten le voy a poder mostrar, es decir depuendiendo de su posición puede ver más o menos, por tanto voy aver la cantidad de personas delante. 
        cantidadDePersonaDelante = 0;
        if (miFilaDeDatosAsistente[2] == False): # en el caso de que ese asistente, no sea privilegiado, tengo que averiguar la cantidad de personas que tiiene delante.
            fechaDeSolicitudDelRobot = miFilaDeDatosAsistente[1];
            #print ("funcion_registrarAsistente()---  el asistenten, no es privilegiado. "); 
            for miAsistenteDatos in miDiccionarioEventoYasistentesDatos[idEvento]:
                if (miAsistenteDatos[1] != None):  # esto es para no tener en cuenta a las personas que ya estan controlando un robot, ya que si pasan a controlarlo, esta feche (posicionDeColaConFecha) se les borra. 
                    if (miAsistenteDatos[1] < fechaDeSolicitudDelRobot):
                        #print ("funcion_registrarAsistente()--- una pserona mas delante");
                        cantidadDePersonaDelante = cantidadDePersonaDelante + 1;
                #else:
                #    print ("funcion_registrarAsistente()--- esa persona no se me cuela. la fecha a comprobar de los demas: ", miAsistenteDatos[1], " la fecha de ese asistente:  ", fechaDeSolicitudDelRobot);
            
        #print ("funcion_registrarAsistente()--- cantidad de personas delanrte: ", cantidadDePersonaDelante);
        # ahora consigo los robots y ver que cantidad de robots rechazados ese token en ese evento tiene, para de esta manera no mostrarle los robot que no están rechazados. 
        miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento==idEvento, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();
            
        # hay 3 pasos para conseguir un robot.
        # Paso1. esta es la parte que analiza la cantidad de robots que estan en servicio. 
        #aqui lo que hago es quitar elementos de la lista que acabo de obtener de la BBDD en funcion de si el robot_idRobt esta en la lista de miListaRobotsQueNoEstanEnServicio.  
        for i in miListaDisponibleRobot[:]:  # con esto lo que hago es recorrer una copia de la lista, ya que la original la voy a modificcar: miListaDisponibleRobot[:]: 
            if (i.robot_idRobot in miListaRobotsQueNoEstanEnServicio):
                miListaDisponibleRobot.remove (i);
            
        # paso2. de todos los robots que esten en servicio, voy a aliminar los que ya esten siendo usados. 
        for i in miListaDisponibleRobot[:]:
            miAsistente = Asistente.query.filter (Asistente._Asistente__robot_idRobot == i.robot_idRobot, Asistente._Asistente__fechaTomaDelRobot <= datetime.now(), Asistente._Asistente__fechaAbandonoDelRobot >= datetime.now()).first ();
            if (miAsistente): # en el caso de que el robot este siendo utilizado, (segun la BBDD). 
                miListaDisponibleRobot.remove (i);
                    
        #paso3. #aqui lo que hago es quitar elementos de la lista en funcion de las personas que tenga delante ese asistente.  
        for i in range (0 , cantidadDePersonaDelante): 
            if (miListaDisponibleRobot):
                miListaDisponibleRobot.pop(0);
            
        #print ("funcion_registrarAsistente()--- ", miListaDisponibleRobot);
        # sigo con la logica de los robots rechazados, deberia de coprobar prinero que todo si ese token en ese evento existe, en el caso que no, simplemente cojo el primer robot. 
        miVariabletokenDeSesionYevento = session ['token'] +"-" +str(idEvento);
        miRobot = None;
            
        if (not miListaDisponibleRobot):  # en el caso de que la lista este vacia. 
            #print ("funcion_registrarAsistente()--- No se ha conseguido un robot. ");
            miListaRobots = [];
            # esta linea la hago para ver todos los robots del evento. Aunqque despeus esto lo borrare. 
            miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.evento_idEvento==idEvento, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();
            for miDisponibleRobotObjeto in miListaDisponibleRobot: 
                miRobot = Robot.query.filter_by (_Robot__idRobot=miDisponibleRobotObjeto.robot_idRobot).first ();
                miListaRobots.append (miRobot);
            #miEvento = Evento.query.filter_by (_Evento__idEvento = idEvento).first ();
            return (render_template("registrarasistente.html", miParametroMiEventoNombreDelEvento=miEvento.nombreDelEvento, miListaRobotsParametro=miListaRobots));
        else:
            if (miVariabletokenDeSesionYevento in miDiccionarioGlobalTokensListaDeRobotsRechazados):# si he rechazado algun robot, voy a ver que otro robot le puedo ofrecer al asistente. 
                #print ("funcion_registrarAsistente()--- ese token y evento, ya ha rechazado algun robot. : ", miDiccionarioGlobalTokensListaDeRobotsRechazados);
                for miDisponibleRobotObjeto in miListaDisponibleRobot:
                    if (miDisponibleRobotObjeto.robot_idRobot not in miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento]):
                        miRobot = Robot.query.filter_by (_Robot__idRobot=miDisponibleRobotObjeto.robot_idRobot).first();
                if (miRobot == None):  # en este caso si no he conseguido ningú robot, eso significa que he pasado todos, voy a olvodarme de todos los que he rechazado. 
                    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento].clear ();
                    miRobot = Robot.query.filter_by (_Robot__idRobot=miListaDisponibleRobot[0].robot_idRobot).first();
                return render_template ("robotlisto.html", miRobotParametro=miRobot, miParametroMiEventoNombreDelEvento=miEvento.nombreDelEvento, miParametroMiEventoIdEvento=miEvento.idEvento);
            else:
                #miEvento = Evento.query.filter_by (_Evento__idEvento = idEvento).first ();
                miRobot = Robot.query.filter_by (_Robot__idRobot=miListaDisponibleRobot[0].robot_idRobot).first(); 
                return render_template ("robotlisto.html", miRobotParametro=miRobot, miParametroMiEventoNombreDelEvento=miEvento.nombreDelEvento, miParametroMiEventoIdEvento=miEvento.idEvento);
                    

@app.route ('/aceptarrobot/<int:idRobot>/<int:idEvento>')
def funcion_aceptarRobot (idRobot, idEvento):
    #en el caso de que no tenga token, que se vaya a una pagina de error, ya que el token se utilza en funciones. 
    if ('token' not in session):
        return "<p>  no se puede entrar a esta URL, no se ha declarado el evento. utiliza el QR para acceder. ";
        
    miAsistente = Asistente.query.filter (Asistente._Asistente__tokenDeSesion==session['token'], Asistente._Asistente__fechaTomaDelRobot <= datetime.now(), Asistente._Asistente__fechaAbandonoDelRobot >= datetime.now()).first ();
    if (miAsistente):   # en este momento el asistente esta controlando un robot
        #print ("funcion_aceptarRobot() --- en este momento el asistente esta controlando un robot");
        miRobot = miAsistente.funcion_consultaRobot (idRobot);
        miEvento = miAsistente.funcion_consultaEvento (miAsistente.evento_idEvento);
        #mirespuestaJson = {'idRobot': miRobot.idRobot, 'macAddressDelRobot': miRobot.macAddressDelRobot};
        #return jsonify(mirespuestaJson), 200;
        return render_template ("robotmanejando.html", miRobotParametro=miRobot, miParametroMiEventoNombreDelEvento=miEvento.nombreDelEvento);
    else:
        #print ("funcion_aceptarRobot() --- el aistenten no esta controlando un robot. ");
        miPosicionDeColaConFecha = None;# esta variable la uso pra extraer la posicionDeColaConFecha de del token en ese evento, que es lo que hago en el siguiente for. 
        miEsPrivilegiado = False;  # esta variable la uso para extraer el valor de si el asistente es o no privilegiado.  algo parecido a la variable: miPosicionDeColaConFecha
        #print ("funcion_aceptarRobot() --- esta es la matriz:  ", miDiccionarioEventoYasistentesDatos[idEvento]);
        for indiceNumerico, i in enumerate(miDiccionarioEventoYasistentesDatos[idEvento]):
            if (session['token'] == i[0]):  # en el caso de que encuentre el token de sesion dentro del indice cero de la lista que tiene [tokenDeSesion, posicionDeColaConFecha, esPrivilegiado], entonce me quedo con la posicionDeColaConFecha, para posteriormente ver si es null.
                miPosicionDeColaConFecha = i[1];
                miEsPrivilegiado = i[2];
                break;
        # en el caso de que no tenga posicion de cola con fecha y no sea privilegiado, eso significa que en algun momento se le ha borrado, por lo tanto como no esta controlando un robot y tampoco tiene posicionDeColaConFecha, tengo que volver a 
        #funcion_registrarse, para que obtenga aqui  una nueva hora de solicitud de un robot. 
        if (miPosicionDeColaConFecha == None) and (miEsPrivilegiado == False):
            #print ("funcion_aceptarRobot() --- la posicion de cola con fecha al parecer es NULL. ");
            return redirect (url_for ('funcion_registrarAsistente', idEvento=idEvento));            
        else: # en el caso de que tenga posicionDeColaConFecha, entonces me voy a meter dentro de un robot, y borrare la posicionDeColaConFecha. 
            #print ("funcion_aceptarRobot() --- si que hay posicionDeColaConFecha.  ");
            miAsistente = Asistente.query.filter (Asistente._Asistente__robot_idRobot==idRobot, Asistente._Asistente__fechaTomaDelRobot <= datetime.now(), Asistente._Asistente__fechaAbandonoDelRobot >= datetime.now()).first ();
            if (miAsistente):  # en el caso de que alguien se haya colado, y se ponga a controlar ese robot, lo que tengo que hacer es volver a funcion_registrarAsistente para conseguir otro robot. 
                return redirect (url_for ('funcion_registrarAsistente', idEvento=idEvento));  
            else:
                if (idRobot in miListaRobotsQueNoEstanEnServicio):  # aqui lo que hago es comprobar si el robot esta o no en servicio, en el caso de que no lo este, entonces lo mando a la  funcion_registrarAsistente para que consiga otro robot. 
                    return redirect (url_for ('funcion_registrarAsistente', idEvento=idEvento));  
                else:
                    miAsistente = Asistente (tokenDeSesion=session['token'], evento_idEvento=idEvento, robot_idRobot=idRobot, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now() + timedelta(minutes=5));
                    db.session.add (miAsistente);
                    db.session.commit ();
                    miRobot = miAsistente.funcion_consultaRobot (idRobot);
                    miEvento = miAsistente.funcion_consultaEvento (idEvento);
                    # aqui lo que hago es, ese token buscarlo dentro de la matriz que proporciona el evento, y cuando lo encuentre, a ese token el valor de indice 1, lo establezco en null, para que posicionDeColaConFecha = None.
                    for indiceNumerico, i in enumerate (miDiccionarioEventoYasistentesDatos[idEvento]):
                        if (session['token'] == i[0]): # si encientro el token. 
                            i[1] = None;  # la posicion de cola con fecha la establezco en NULL. 
                            i[2] = False; # tambien establezco que ya no es privilegiado. 
                            break;
                    # como ya e definitivo que paso a controlar un robot, lo que hago es que la lista del diccionario que almecena los robots que han sido rechazados, no tenga ningun elemento, para que cuando quiera elehir de nuevo un robot, 
                    # (despues de que haya acabado el tiempo de utilizar uno o le haya expulsado un administradir) que no haya ningun problema. 
                    miVariabletokenDeSesionYevento = session ['token'] +"-" +str(idEvento);
                    if (miVariabletokenDeSesionYevento in miDiccionarioGlobalTokensListaDeRobotsRechazados): # este if lo tengo porque unas veces el asistente no rechaza un robot, por lo tanto nunca se mete en este diccionario, entonces lo que estoy haciendo es ver primero si esta.
                        miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento].clear (); 
                    return (render_template ("robotmanejando.html", miRobotParametro=miRobot, miParametroMiEventoNombreDelEvento=miEvento.nombreDelEvento));
                

    
@app.route ('/rechazarrobot/<int:idRobot>/<int:idEvento>')
def funcion_rechazarRobot (idRobot, idEvento):
    #en el caso de que no tenga token, que se vaya a una pagina de error, ya que el token se utilza en funciones. 
    if ('token' not in session):
        return "<p>  no se puede entrar a esta URL, utiliza el QR para acceder. ";

    #print ("funcion_rechazarRobot --- ");
    # aqui lo que hago es dejar preparada la calve del diccionario miDiccionarioGlobalTokensListaDeRobotsRechazados para que su clave  sea el token y el idEvento, para que este elemento sea unico, lo que voy a dejar en el valor va a ser una lista de
    #idRobot para saber que estos son los que se han rechazado. 
    miVariabletokenDeSesionYevento = session ['token'] +"-" +str(idEvento);
    
    # en el caso de que ese token con evento, no este en la clave del diccionrio, lo que hago es inicializarlo como lista, que recordar que ahi van a ir los robots que han sido rechazados.  
    if (miVariabletokenDeSesionYevento not in miDiccionarioGlobalTokensListaDeRobotsRechazados):  
        miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento]  = [];
    
    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento].append (idRobot);
    #print ("funcion_rechazarRobot --- ", miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento]);
    
    return redirect (url_for ("funcion_registrarAsistente", idEvento=idEvento));
    
    
########################### endpoints Administrador. ################################################################################################################################################################################################# 
@app.route ("/administradorsignup", methods = ['GET', 'POST'])
def funcionAdministradorsignup ():
    miFormulario = formulario.FormularioAcceder (request.form);
    if (request.method == 'POST'):
        miContrasenaHaseada = generate_password_hash (miFormulario.contrasena.data);
        miAdministrador = Administrador (correoElectronico=miFormulario.correoElectronico.data, contrasena=miContrasenaHaseada);
        db.session.add (miAdministrador);
        db.session.commit ();
        return redirect (url_for ('funcionAdministradorLogin'));

    return (render_template ("administradorsignup.html", miFormularioParametro=miFormulario));


@app.route ("/administradorlogin", methods = ['GET', 'POST'])
def funcionAdministradorLogin ():
    #print ("funcionAdministradorLogin --- se ejecuta");
    miFormulario = formulario.FormularioAcceder (request.form);
    miVariableUsuarioIncorrecto = False;
    miVariableContrasenaIncorrecta = False;
    if (request.method == 'POST'):
        miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=miFormulario.correoElectronico.data).first ();
        if (miAdministrador != None):
            #print ("funcionAdministradorLogin()---  esta es la contrasena:", miFormulario.contrasena.data);
            if (miAdministrador.validarContrasena (miFormulario.contrasena.data)):
                session['correoElectronico'] = miAdministrador.correoElectronico;
                return redirect (url_for ('funcionAdministradorHome'));
            else:
                #print ("funcionPanelAdministrador ---  contrasena incoreecta.  ");
                miVariableContrasenaIncorrecta = True;
        else:
            #print ("funcionPanelAdministrador ---  usuario incoreecto.  ");
            miVariableUsuarioIncorrecto = True;
            
    return (render_template("administradorlogin.html", miFormularioParametro = miFormulario, miParametroUsuarioIncorrecto = miVariableUsuarioIncorrecto, miParametroContrasenaIncorrecta = miVariableContrasenaIncorrecta));
    

@app.route ("/administradorcerrarsesion")
def funcionAdministradorCerrarSesion ():
    #print ("funcionAdministradorCerrarSesion --- se ejecuta.");
    session.pop ('correoElectronico');
    return redirect (url_for ('funcionAdministradorLogin'));
  
@app.route('/administradorhome/<int:parametroVerdadHayEventos>')   
@app.route('/administradorhome')   
def funcionAdministradorHome(parametroVerdadHayEventos=1):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    #print ("parametroVerdadHayEventos()---", parametroVerdadHayEventos);
    
    miVariableCantidadDeEventosTotales = len (miAdministrador.funcion_conseguirTodosLosEventos());
    miVariableCantidadRobotsTotales = len (miAdministrador.funcion_conseguirTodosLosRobots ());
    miVariableCantidadAsistentensTotales = 0;
    miListaAuxiiarAsistentesTotales = [];
    if (miDiccionarioEventoYasistentesDatos):  # en el caso de que el diccionario no este vacio. 
        for clave, valor in miDiccionarioEventoYasistentesDatos.items():
            for i in miDiccionarioEventoYasistentesDatos[clave]: # para cada lista de la matriz. 
                if i[0] not in miListaAuxiiarAsistentesTotales:  # si esa lista de indice cer, es decir si el tokenDeSesion,  no está en la lista miListaAuxiiarAsistentesTotales, entonces lo meto, de esta manera no tengo repetidos. 
                    miListaAuxiiarAsistentesTotales.append (i[0]);
    miVariableCantidadAsistentensTotales = len (miListaAuxiiarAsistentesTotales);
    
    miVariableCantidadAsistentensEsperando = 0;
    miListaAuxiliarAsistentesEsperando = [];
    if (miDiccionarioEventoYasistentesDatos):  # en el caso de que el diccionario no este vacio. 
        for clave, valor in miDiccionarioEventoYasistentesDatos.items():
            for i in miDiccionarioEventoYasistentesDatos[clave]: # para cada lista de la matriz. 
                if (i[0] not in miListaAuxiliarAsistentesEsperando) and (i[1] != None): 
                    miListaAuxiliarAsistentesEsperando.append (i[0]);
    miVariableCantidadAsistentensEsperando = len (miListaAuxiliarAsistentesEsperando);
    return (render_template ("administradorhome.html", parametroVerdadHayEventos=parametroVerdadHayEventos, parametroCantidadDeEventosTotales=miVariableCantidadDeEventosTotales, parametroCantidadDeRobotsTotales=miVariableCantidadRobotsTotales, 
    parametroCantidadAsistentesTotales=miVariableCantidadAsistentensTotales, parametroCantidadAsistentesEsperando= miVariableCantidadAsistentensEsperando));

    
@app.route ('/administradorpanelrobot/<idEvento>')
@app.route ('/administradorpanelrobot')
def funcionAdministradorPanelRobot (idEvento = '-1'):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    miListaRobots = miAdministrador.funcion_conseguirTodosLosRobots();
    idEvento = int(idEvento);

    miListaDeEventosEnLosQueHayRobots = miAdministrador.funcion_conseguirTodosLosEventos ();
    miMostrarRobotsNingunEvento = False;

    if (idEvento > 0):
        miListaRobots = [];
        miListaDisponibleRobot = miAdministrador.funcion_conseguirDisponibleRobotPorEvento (idEvento);
        for miDisponibleRobotObjeto in miListaDisponibleRobot:
            miRobot = miAdministrador.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robot_idRobot);
            if (miRobot not in miListaRobots): # aqui sólo añado los robots que no se repiten, por eso compruebo primero si esta. 
                miListaRobots.append (miRobot);
    if (idEvento < 0):
        miMostrarRobotsNingunEvento = True;
        miListaRobots = [];
        miListaRobots = miAdministrador.funcion_conseguirRobotsQueNoEstanEnNingunEvento ();

    return render_template ("administradorpanelrobot.html", miListaRobotsParametro=miListaRobots, miListaDeEventosEnLosQueHayRobotsParametro=miListaDeEventosEnLosQueHayRobots, miParametroMostrarRobotsNingunEvento=miMostrarRobotsNingunEvento);

@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>/<int:idEvento>')
@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>')
def funcionAdministradorPanelRobotBorrar (idRobot, idEvento=0):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    if (miAdministrador.funcion_verSiPuedoBorrarRobot (idRobot) == False):
        raise Exception ("administradorpaneleventoborrar.html --- ese administrador, no puede eliminar ese robot.");

    miAdministrador.funcion_borrarRobot (idRobot);
    if (idEvento > 0):
        return redirect (url_for ('funcionAdministradorModificarRobotsEvento', idEvento = idEvento));
    else:
        return redirect (url_for ('funcionAdministradorPanelRobot'));
    
@app.route ('/administradorcrearrobot', methods = ['GET', 'POST'])
def funcionAdministradorCrearRobot ():
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCreaRobot (request.form);
    # ya que administradorcrearrobot.html lo utilizo en crear robot, modificar roboot y en modificar robot cuando estoy dentro del evento, el idEvento es una variable que se utiliza a la hora de renderizar, es decir
    # ver que elementos HTML son los que se van a mostrar, por lo tanto en esta linea voy a poner un idEvento que nunca se puedar en el sistema, el evento 0. 
    idEvento = 0;
    
    if (request.method == 'POST') and (miFormulario.validate ()): 
        fotoRecibidaDelFormulario = request.files['fotoDelRobot'];
        binarioDeFoto = fotoRecibidaDelFormulario.read();
        # de esta forma detrmino si hay o no hay foto, ya que en el caso de que el peso de la foto sea 0, eso significa que no se ha adjuntado la foto. 
        if (len (binarioDeFoto) == 0):
            # de esta forma en el caso de que la foto no se haya insertado, entonces a la BBDD le paso el valor de NULL. 
            binarioDeFoto = None;
        else:
            print ("funcionAdministradorCrearRobot()--- este es el archivo:  ", fotoRecibidaDelFormulario.filename);

            #En esta parte voy a poner la validación del documento que se sube a la página web, la foto debe de pesar como maximo 10MB. 
            if ((len(binarioDeFoto)/1024) > 10240):
                raise Exception ("administradorcrearrobot.html --- el tamaño máxm de las fotos es de 10MB. ");
            else:
                # en esta parte voy a poner la validación del tipo de documento, debe ser .JPG o .JPEG o .PNG
                miExpresionRegularParaJPG = r".+\.jpg$";
                miExpresionRegularParaJPEG = r".+\.jpeg$";
                miExpresionRegularParaPNG = r".+\.png$";

                miVerdadEsJPG = bool(re.match (miExpresionRegularParaJPG, fotoRecibidaDelFormulario.filename));
                miVerdadEsJPEG = bool(re.match (miExpresionRegularParaJPEG, fotoRecibidaDelFormulario.filename));
                miVerdadEsPNG = bool(re.match (miExpresionRegularParaPNG, fotoRecibidaDelFormulario.filename));
                if (miVerdadEsJPG == False) and (miVerdadEsJPEG == False) and (miVerdadEsPNG == False):
                    raise Exception ("administradorcrearrobot.html --- la extesión del archivo no es valida, las extensiones permitidas son .jpg .jpeg y .png");
                else:
                    print ("funcionAdministradorCrearRobot()--- la expresion regular si que cuadra, por tanto no da error. ");
            print ("funcionAdministradorCrearRobot()--- este es el tamaño:  ", len(binarioDeFoto));
            print ("funcionAdministradorCrearRobot()--- este es el tamaño en KB:   ", len(binarioDeFoto)/1024);

            
        miAdministrador.funcion_crearRobot (miFormulario.macAddressDelRobot.data, miFormulario.nombreDelRobot.data, binarioDeFoto, miFormulario.descripcionDelRobot.data);
        return redirect(url_for('funcionAdministradorPanelRobot'));

    return render_template ('administradorcrearrobot.html', miFormularioParametro = miFormulario, miParametroAccionHtml = "crear",miParametroIdEvento=idEvento);
    
# en est parte dejo la posibilidad de que este endpoint no reciba el evento, ya que puedde ser que se modifique un robot desde el panel robot, el cual muestra todos los robots que no estan en ningun evento, y recordar que en esta parte cualquier administrador
#puede borrar un robot, por lo tanto despues de borrarlo la pantalla de muestra no tiene porque ser la de gestion de robots en evento, si no que puede ser que se quede en la misma pudiendo eliminar mas robots. 
@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>', methods = ['GET', 'POST'])
@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobotModificar (idRobot, idEvento=0):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    #print ("funcionAdministradorPanelRobotModificar()--- ", idEvento);
    miFormulario = formulario.FormularioCreaRobot (request.form);
    
    if (request.method == 'POST'):
        if (miFormulario.validate()):
            miFormulario = formulario.FormularioCreaRobot (request.form);
            fotoRecibidaDelFormulario = request.files['fotoDelRobot'];
            binarioDeFoto = fotoRecibidaDelFormulario.read();
            if (len(binarioDeFoto) == 0):
                #print ("funcionAdministradorModificaRobot()--- No hay foto, se utilizara la anterior. ");
                binarioDeFoto = None;
            miAdministrador.funcion_modificarRobot (idRobot, miFormulario.macAddressDelRobot.data, miFormulario.nombreDelRobot.data, binarioDeFoto, miFormulario.descripcionDelRobot.data);
            if (idEvento > 0):
                return redirect (url_for ('funcionAdministradorModificarRobotsEvento', idEvento=idEvento));
            else:
                return redirect(url_for('funcionAdministradorPanelRobot')); 
        else:
            # en el caso de que no se valide el formulario, lo que hago es que devuelvo el formulario con los datos que se acaban de rellenar por el request.form y en este ya está almacenado el error. 
            return render_template ("administradorcrearrobot.html", miFormularioParametro=miFormulario, miParametroAccionHtml="modificar", miParametroIdEvento=idEvento);
    else:
        # esto es para comprobar si se esta edtando un robot que no esta asociado a ningun evento. 
        if (miAdministrador.funcion_verSiUnRobotEstaEnAlMenosUnEvento (idRobot)):
            # dado que s un adinistrador conoce el idRobot de un robot que no se le muestra, el puede poner en la URL que lo va a modificar, con este IF yo comppruebo si ese administrador lo va a utilizar en algun momento. En el caso de que no, no le dejo modificar.
            if (miAdministrador.funcion_verSiEseRobotEsDeEseAdministrador (idRobot) == False):
                raise Exception ("administradorpaneleventoborrar.html --- ese administrador, no utiliza, ni va a utilizar ese robot, por lo tanto no lo va a modificar.");
            else:
                #en el caso de que un administrador vea un robot, sabiendo que esta en la tabla de disponible, pero que ademas ese robot lo estan utilizando actualmente, entonces no se le va a mostrar la opcion de modificar, pero lo que pasa es que si el pone en la URL
                # a este robot, entonecs sí que lo puede modificar, por lo tanto hago este if que vuelve a comprobar si ese administrador lo puede o no modificar, en el caso de que no pueda, le mando un error. 
                if (miAdministrador.funcion_verSiPuedoModificarRobot (idRobot) == False):
                    raise Exception ("administradorpaneleventoborrar.html --- ese administrador, no puede modificcar ese robot, ya que otro adminsitrador lo esta usando actualmente. ");

        miRobot = miAdministrador.funcion_conseguirRobotPorIdRobot (idRobot);
        miFormulario = formulario.FormularioCreaRobot(obj=miRobot);
        return render_template ("administradorcrearrobot.html", miFormularioParametro=miFormulario, miParametroAccionHtml="modificar", miParametroIdEvento=idEvento);
        
        
@app.route ('/administradorpanelevento/<int:miVerdadErrorDeEventoInexistente>')
@app.route ('/administradorpanelevento')
def funcionAdministradorPanelEvento (miVerdadErrorDeEventoInexistente = 0):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();

    miListaDeRobots = miAdministrador.funcion_conseguirTodosLosRobots ();
    # esto lo estoy haciendo debido a que puede en el momento de que no yahan datos en el sistema y se cree por primera vez un administrador y este acceda el sistema, lo que va a pasar es que 
    #dentro de el, no van a haber robots, evidantemente, y en el caso de que pulse administradr eventos, que salga un mensaje de error que diga "no hay eventos en el sistema" ya que si no hay 
    # robots, no puede haber eventos.
    if (not miListaDeRobots):
        return redirect (url_for ('funcionAdministradorHome', parametroVerdadHayEventos=0));
    else:
        #print ("funcionAdministradorPanelEvento()---miListaDeRobots: ", miListaDeRobots);
        miListaEventos = miAdministrador.funcion_conseguirTodosLosEventosDeEseAdministrador ();
        return render_template ("administradorpanelevento.html", miListaEventosParametro=miListaEventos, miParametroVerdadErrorDeEventoInexistente=miVerdadErrorDeEventoInexistente);
    
@app.route ('/administradorpaneleventoborrar/<int:idEvento>')
def funcionAdministradorPanelEventoBorrar (idEvento):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    if (miAdministrador.funcion_verSiEseEventoEsDeEseAdministrador(idEvento)):
        miAdministrador.funcion_borrarEvento (idEvento);
        return redirect (url_for ('funcionAdministradorPanelEvento'));
    else:
        raise Exception ("administradorpaneleventoborrar.html --- para ese adminstrador, ese evento no existe");


@app.route ('/administradorcrearevento', methods = ['GET', 'POST'])
def funcionAdministradorCrearEvento ():
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCrearEvento (request.form);
    
    miVariableSeHaRellenadoFormularioCorrectamente = True;
    if (request.method == 'POST'):
        miCantidadDeRobots =  int(request.form.get('cantidadDeRobots'));
        miVerdadSePuedeCrearEvento = False;
        miListaDisponibleRobot = [];
        
        # este for lo uso para detectar si se ha rellenado al menos un robot, en el caso de que no se haya rellenado ninguno, no creo el evento. 
        # A la cantidad de robots le tengo que sumar uno, ya que el range()  va desde el inicio hasta el final menos uno, por lo tanto si quiero que 
        #  recorra todos los robots que se me han mostrado en las vistas, tengo que sumar uno. 
        for i in range(1, miCantidadDeRobots+1): 
            miFechaComienzoEnEventoRecibido = request.form.get(f'fechaComienzoEnEvento{i}');
            miHoraComienzoEnEventoRecibido  = request.form.get(f'fechaComienzoEnEventoHora{i}');
            # el segundo elemento del and, es para que en el caso de que no se haya rellenado la hora, que no se escriba el caracter T.  
            if (miFechaComienzoEnEventoRecibido != "" and miHoraComienzoEnEventoRecibido != ""):
                miFechaComienzoEnEventoRecibido += "T";
                miFechaComienzoEnEventoRecibido += miHoraComienzoEnEventoRecibido;
            miFechaFinEnEventoRecibido = request.form.get(f'fechaFinEnEvento{i}');
            miHoraFinEnEventoRecibido = request.form.get(f'fechaFinEnEventoHora{i}');
            if (miFechaFinEnEventoRecibido != "" and miHoraFinEnEventoRecibido!= ""):
                miFechaFinEnEventoRecibido += "T";
                miFechaFinEnEventoRecibido += miHoraFinEnEventoRecibido;
            miRobotRecibido = request.form.get (f'robot_idRobot{i}');
            
            if (miFechaComienzoEnEventoRecibido != "") and (miFechaFinEnEventoRecibido != ""):
                miVerdadSePuedeCrearEvento = True;
                miListaDisponibleRobot.append ([miFormulario.idEvento.data, miRobotRecibido, miFechaComienzoEnEventoRecibido, miFechaFinEnEventoRecibido]);
                
        if (miVerdadSePuedeCrearEvento == True):
            miAdministrador.funcion_crearEvento (miListaDisponibleRobot, miFormulario.idEvento.data, miFormulario.nombreDelEvento.data, miFormulario.calle.data, miFormulario.numero.data,
            miFormulario.edificioDondeSeCelebra.data, miFormulario.codigoPostal.data);
            return redirect (url_for ('funcionAdministradorPanelEvento'));
        else:
            miVariableSeHaRellenadoFormularioCorrectamente = False;
    
    miListaRobots = miAdministrador.funcion_conseguirTodosLosRobots ();            
    return render_template ("administradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "crear", miListaRobotsParametro=miListaRobots, miParametroVariableNoSeHaRellenadoFormularioCorrectamente= miVariableSeHaRellenadoFormularioCorrectamente);

@app.route ('/administradormodificardatosevento/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdministradorModificarDatosEvento (idEvento):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCrearEvento (request.form);
    miVariableSeHaRellenadoFormularioCorrectamente = True;
    
    if (request.method == 'POST'):
        miAdministrador.funcion_modificarDatosDelEvento (idEvento, miFormulario.idEvento.data,  miFormulario.nombreDelEvento.data, miFormulario.calle.data, miFormulario.numero.data, miFormulario.edificioDondeSeCelebra.data,
        miFormulario.codigoPostal.data);
        return redirect(url_for('funcionAdministradorPanelEvento'));
        

    if (miAdministrador.funcion_verSiEseEventoEsDeEseAdministrador (idEvento)):
        miEvento = miAdministrador.funcion_conseguirEventoPorIdEvento (idEvento);
        miFormulario = formulario.FormularioCrearEvento (obj=miEvento);
        return render_template ("administradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar", miParametroVariableNoSeHaRellenadoFormularioCorrectamente= miVariableSeHaRellenadoFormularioCorrectamente);
    else:
        return redirect(url_for('funcionAdministradorPanelEvento', miVerdadErrorDeEventoInexistente=1));
    
    
@app.route ('/administradormodificarrobotsevento/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdministradorModificarRobotsEvento (idEvento):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first(); 
    
    if (request.method == 'POST'):
        if ('nameformulariomodificar' in request.form):
            print ("funcionAdministradorModificarRobotsEvento()---", request.form.get('robot_idRobot'));
            print ("funcionAdministradorModificarRobotsEvento()---", request.form.get('fechaComienzoEnEventoAntigua'));
            print ("funcionAdministradorModificarRobotsEvento()---", request.form.get('fechaFinEnEventoAntigua'));
            print ("funcionAdministradorModificarRobotsEvento()---", request.form.get('fechaComienzoEnEvento'));
            print ("funcionAdministradorModificarRobotsEvento()---", request.form.get('fechaFinEnEvento'));


            miAdministrador.funcion_modificarRobotDelEvento (idEvento, request.form.get('robot_idRobot'), request.form.get('fechaComienzoEnEventoAntigua'), request.form.get('fechaFinEnEventoAntigua'), request.form.get('fechaComienzoEnEvento'), request.form.get('fechaFinEnEvento'));
            return redirect (url_for ('funcionAdministradorModificarRobotsEvento', idEvento=idEvento));
        else:
            if ("nameformulariosumarrobot" in request.form):
                miIdRobotRecibido = request.form.get('idRobot');
                miFechaComienzoEnEventoRecibido = request.form.get ('fechaComienzoEnEvento');
                miHoraEnEventoRecibido = request.form.get ('fechaComienzoEnEventoHora');
                if (miFechaComienzoEnEventoRecibido != "" and miHoraEnEventoRecibido != ""):
                    miFechaComienzoEnEventoRecibido += "T";
                    miFechaComienzoEnEventoRecibido += miHoraEnEventoRecibido;
                
                miFechaFinEnEventoRecibido = request.form.get ('fechaFinEnEvento');
                miHoraEnEventoRecibido = request.form.get ('fechaFinEnEventoHora');
                if (miFechaFinEnEventoRecibido != "" and miHoraEnEventoRecibido != ""):
                    miFechaFinEnEventoRecibido += "T";
                    miFechaFinEnEventoRecibido += miHoraEnEventoRecibido;
                miAdministrador.funcion_sumarRobotAlEvento (idEvento, miIdRobotRecibido, miFechaComienzoEnEventoRecibido, miFechaFinEnEventoRecibido);
                return redirect (url_for ('funcionAdministradorModificarRobotsEvento', idEvento=idEvento));
            else:
                if ("nameformularioeliminar" in request.form):
                    miAdministrador.funcion_eliminarRobotDelEvento (idEvento, request.form.get('robot_idRobot'), request.form.get('fechaComienzoEnEventoAntigua'), request.form.get('fechaFinEnEventoAntigua'));
                    return redirect (url_for ('funcionAdministradorModificarRobotsEvento', idEvento=idEvento));
                else:
                    raise Exception ("administradormodificarrobotsevento.htmml --- formulario invalido.");
    
    if (miAdministrador.funcion_verSiEseEventoEsDeEseAdministrador (idEvento)):
        miDiccionarioRobotsActualmenteEstanEnEvento = {};
        miListaDisponibleRobot = miAdministrador.funcion_conseguirDisponibleRobotPorEventoYporEstarContempladaLaFechaDelSistema (idEvento);
        for miDisponibleRobotObjeto in miListaDisponibleRobot:  #  este for me vale para rellenar los robots del evento. tabla1.
            miRobot = miAdministrador.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robot_idRobot);
            if (miRobot not in miDiccionarioRobotsActualmenteEstanEnEvento):
                miDiccionarioRobotsActualmenteEstanEnEvento[miRobot] = [];  # de esta manera inicializo el vector. 
            miDiccionarioRobotsActualmenteEstanEnEvento[miRobot].append (miDisponibleRobotObjeto);    
        #este for es para rellenar en el diccionario que almacena los robots de la tabla 1, par que el diccionario tenga tambien de cada uno de los robots en conocimiento de si debe mostrar los botones de borrar, modificar y enServicio. 
        for clave in miDiccionarioRobotsActualmenteEstanEnEvento:
            miVariablePuedoeliminar = miAdministrador.funcion_verSiPuedoBorrarRobot (clave.idRobot);
            miVariableQueBotonEnServicioEs = clave.idRobot in miListaRobotsQueNoEstanEnServicio;  # aqui lo que hago es ver si ese robot_idRobot esta en la lista, en el caso de que no esté me devuelve false. 
            miDiccionarioRobotsActualmenteEstanEnEvento[clave] = {"subclaveListas":miDiccionarioRobotsActualmenteEstanEnEvento[clave], "subclavePuedoeliminar": miVariablePuedoeliminar, "subclaveQueBotonEnServicioEs": miVariableQueBotonEnServicioEs};

        miDiccionarioRobotsActualmenteNoEstanEnEvento = {};
        miListaDisponibleRobot = miAdministrador.funcion_conseguirDisponibleRobotPorEventoYporNoEstarContempladaLaFechaDelSistema (idEvento);
        for miDisponibleRobotObjeto in miListaDisponibleRobot: 
            miRobot = miAdministrador.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robot_idRobot);
            if (miRobot not in miDiccionarioRobotsActualmenteNoEstanEnEvento):
                miDiccionarioRobotsActualmenteNoEstanEnEvento[miRobot] = [];
            miDiccionarioRobotsActualmenteNoEstanEnEvento[miRobot].append (miDisponibleRobotObjeto);  
        for clave in miDiccionarioRobotsActualmenteNoEstanEnEvento:
            miVariablePuedoeliminar = miAdministrador.funcion_verSiPuedoBorrarRobot (clave.idRobot);
            miVariablePuedoModificar = miAdministrador.funcion_verSiPuedoModificarRobot (clave.idRobot);
            miVariableQueBotonEnServicioEs = clave.idRobot in miListaRobotsQueNoEstanEnServicio; 
            miDiccionarioRobotsActualmenteNoEstanEnEvento[clave] = {"subclaveListas":miDiccionarioRobotsActualmenteNoEstanEnEvento[clave], "subclavePuedoModificar": miVariablePuedoModificar, "subclavePuedoeliminar": miVariablePuedoeliminar, "subclaveQueBotonEnServicioEs": miVariableQueBotonEnServicioEs};

        miListaDeSumarRobot = [];
        for miRobotObjeto in miAdministrador.funcion_conseguirTodosLosRobotsQueNoSonDelAdministradorDeEseEvento (idEvento): # este for me vale para rellenar los formularios de los robots que no estan en ese evento. tabla 3. (la de abajo del todo).  
            #print ("funcionAdministradorModificarRobotsEvento() --", miRobotObjeto);
            miListaDeSumarRobot.append ([miRobotObjeto.idRobot, miRobotObjeto.macAddressDelRobot]);
        return render_template ("administradormodificarrobotsevento.html", miDiccionarioRobotsActualmenteEstanEnEvetoParametro=miDiccionarioRobotsActualmenteEstanEnEvento, miDiccionarioRobotsActualmenteNoEstanEnEvetoParametro=miDiccionarioRobotsActualmenteNoEstanEnEvento, miListaDeSumarRobotParametro=miListaDeSumarRobot, miParametroIdEvento =idEvento);
    else:
        return redirect(url_for('funcionAdministradorPanelEvento', miVerdadErrorDeEventoInexistente=1));
        
@app.route ('/adminstradorpanelrobotponerservicio/<int:idRobot>/<int:robotEnServicio>/<int:idEvento>')
def funcionAdministradorPanelRobotPonerServicio (idRobot, robotEnServicio, idEvento): 
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first(); 
    if (miAdministrador.funcion_verSiPuedoModificarRobot (idRobot) == False):
        raise Exception ("adminstradorpanelrobotponerservicio  --- ese administrador no puede modificar el servicio de ese robot, ya que actualmente la hora de trabajo de este robot no se corresponde con ningun evento de este administrador. ");
    miAdministrador.funcion_activarOdesactivarRobot (idRobot, robotEnServicio);
    return redirect (url_for ('funcionAdministradorModificarRobotsEvento', idEvento=idEvento));

@app.route ('/administradorpaneladministradorgestioncuentas')
def funcionAdministradorGestioncuentas ():
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first()
    miListaAdministradores = miAdministrador.funcion_conseguirTodasLasCuentasMenosLaInstanciada ();
    miDiccionarioAdministradores = {};
    miListaDeEventos = [];
    for i in miListaAdministradores:
        miListaDeEventos = miAdministrador.funcion_conseguirTodosLosEventosPorCorreoElectronico (i.correoElectronico);
        miDiccionarioAdministradores[i.correoElectronico] = miListaDeEventos;
    return render_template ("administradorpanelgestioncuentas.html", miParametroDiccionarioAdministradores = miDiccionarioAdministradores);
        
        
@app.route ('/administradorborrarcuentaadministrador/<correoelectronico>')
def funcionAdministradorBorrarCuentaAdministrador (correoelectronico):
    miAdministrador = Administrador.query.filter_by (_Administrador__correoElectronico=session['correoElectronico']).first ();
    miAdministrador.funcion_borrarCuentaAdministrador (correoelectronico);
    return redirect (url_for ('funcionAdministradorGestioncuentas'));


# este if es algo clásico de python, y es que en el caso de que se importe este main, no se van a ejecutar las lineas que están arriba en el momento de hacer ei import, gracias 
# a este if. De esta manera tengo más control sobre la ejecución y es que a esas funcones de arriba las puedo llamar en cualquier momento.  
if __name__ == '__main__':
    # a la hora de poner los formularios, necesito que tengan un token para verrificar que el me envia los datos de nuevo al servidor, que sea el cliente correcto.  


    # esto lo que hace es aplicar la configuracion de la base datos hecha en el archivo condig.py 
    db.init_app (app);

    # esto es para explicar bajo que contexto,  vamos a crear la DDBB, es decir que vamos a aplicar la configuración que tenemos en el app, el cual hemos configurado en el 
    # archivo config.py con la clase: DevelopmentConfig. De manera que este with es necesario para que se tenga en cuenta la configuración. 
    with app.app_context ():
        db.create_all (); #esto se encarga de crear las tablas que no esten creadas en el modelo. 
        
    app.run(debug=app.config['DEBUG'], port=app.config['PORT']);



