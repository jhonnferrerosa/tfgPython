# el request,  me vale para recibir parámetros por a URL. 
# el redirect me vale para redirigir a los usuarios a otra pagina de mi aplicacion. 
# el url_for genera una url para una de las funciones que tengo en este main.py. 
# el session es para el menajo de las sessiones de los usuarios en la pagina web. 
from flask import Flask, request, render_template, redirect, url_for, session
from models import db
#Desde mi archivo config.py importo esta clase. 
from config import DevelopmentConfig  
from models import Administradores, Robots, Eventos, Asistentes, Vincula, DisponibleRobot, Controla
from datetime import datetime, timedelta 
import formulario
#esto es para que el HTML pida la foto y con esto se la envie. 
from flask import send_file  
# esto lo que hace es convertir la lista da bits de la foto en algo entendible para el navegador. 
from io import BytesIO  
# esto es para sacar valores random del sistema operativo, lo uso para crear mi propio token para los aistentes.
import os 
import random

#from werkzeug.security import generate_password_hash # si quiero usar esto, tengo que hacer:  pip install Werkzeug
from werkzeug.security import generate_password_hash 

# esta libreria es para poder enviar JSON al cliente. 
from flask import jsonify

# esto me vale para utilizar expresiones regulares en pyrhon. 
import re

# esto me vale para generar los codigos QR. 
import qrcode


app = Flask(__name__)
app.config.from_object (DevelopmentConfig);

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
    miAdmin1 = Administradores (correoElectronico="jhon@gmail.com", contrasena=contrasnaHasheda);
    miAdmin2 = Administradores (correoElectronico="ana@gmail.com", contrasena=contrasnaHasheda);
    miAdmin3 = Administradores (correoElectronico="alberto@gmail.com", contrasena=contrasnaHasheda);
    db.session.add (miAdmin1);
    db.session.add (miAdmin2);
    db.session.add (miAdmin3);
    db.session.commit ();

    miEvento1 = Eventos (nombreDelEvento="aula1", fechaDeCreacionDelEvento='2024-10-01', lugarDondeSeCelebra="ifema1", codigoQR="miQR1", administradores_correoElectronico="jhon@gmail.com");
    miEvento2 = Eventos (nombreDelEvento="puertas abiertas1", fechaDeCreacionDelEvento='2024-10-01', lugarDondeSeCelebra="alcala", codigoQR="miQR2", administradores_correoElectronico="jhon@gmail.com");
    miEvento3 = Eventos (nombreDelEvento="eurobot2042", fechaDeCreacionDelEvento='2024-11-27 11:19:48', lugarDondeSeCelebra="ifema2042", codigoQR="http://127.0.0.1:5000/eurobot2042/2024-11-27T11:19:48/ifema2042", administradores_correoElectronico="jhon@gmail.com");
    miEvento4 = Eventos (nombreDelEvento="simo1", fechaDeCreacionDelEvento='2024-10-01', lugarDondeSeCelebra="torrejon", codigoQR="miQR3", administradores_correoElectronico="ana@gmail.com");
    db.session.add (miEvento1);
    db.session.add (miEvento2);
    db.session.add (miEvento3);
    db.session.add (miEvento4);
    db.session.commit ();

    miAsistente1 = Asistentes (identificadorUnicoAsistente="IUA1", apodoAsistente="apodo1", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1");
    miAsistente2 = Asistentes (identificadorUnicoAsistente="IUA2", apodoAsistente="apodo2", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1");
    miAsistente3 = Asistentes (identificadorUnicoAsistente="IUA3", apodoAsistente="apodo3", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1");
    miAsistente4 = Asistentes (identificadorUnicoAsistente="IUA4", apodoAsistente="apodo4", eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala");
    db.session.add (miAsistente1);
    db.session.add (miAsistente2);
    db.session.add (miAsistente3);
    db.session.add (miAsistente4);
    db.session.commit  ();

    miRobot1 = Robots (idRobot=101, macAddressDelRobot="00:00:00:00:00:00", nombreDelRobot="robot1", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot2 = Robots (idRobot=102, macAddressDelRobot="11:11:11:11:11:11", nombreDelRobot="robot2", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot3 = Robots (idRobot=103, macAddressDelRobot="22:22:22:22:22:22", nombreDelRobot="robot3", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot4 = Robots (idRobot=104, macAddressDelRobot="33:33:33:33:33:33", nombreDelRobot="robot4", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot5 = Robots (idRobot=105, macAddressDelRobot="44:44:44:44:44:44", nombreDelRobot="robot5", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot6 = Robots (idRobot=106, macAddressDelRobot="55:55:55:55:55:55", nombreDelRobot="robot6", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot7 = Robots (idRobot=107, macAddressDelRobot="66:66:66:66:66:66", nombreDelRobot="robot7", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot8 = Robots (idRobot=108, macAddressDelRobot="77:77:77:77:77:77", nombreDelRobot="robot8", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot9 = Robots (idRobot=109, macAddressDelRobot="88:88:88:88:88:88", nombreDelRobot="robot9", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot10 = Robots (idRobot=110, macAddressDelRobot="99:99:99:99:99:99", nombreDelRobot="robot10", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot11 = Robots (idRobot=111, macAddressDelRobot="AA:AA:AA:AA:AA:AA", nombreDelRobot="robot11", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot12 = Robots (idRobot=112, macAddressDelRobot="BB:BB:BB:BB:BB:BB", nombreDelRobot="robot12", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    miRobot13 = Robots (idRobot=113, macAddressDelRobot="CC:CC:CC:CC:CC:CC", nombreDelRobot="robot13", disponible=True, fotoDelRobot=None, descripcionDelRobot=None);
    db.session.add (miRobot1);
    db.session.add (miRobot2);
    db.session.add (miRobot3);
    db.session.add (miRobot4);
    db.session.add (miRobot5);
    db.session.add (miRobot6);
    db.session.add (miRobot7);
    db.session.add (miRobot8);
    db.session.add (miRobot9);
    db.session.add (miRobot10);
    db.session.add (miRobot11);
    db.session.add (miRobot12);
    db.session.add (miRobot13);
    db.session.commit ();

    miVincula1 = Vincula (asistentes_identificadorUnicoAsistente="IUA1", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula2 = Vincula (asistentes_identificadorUnicoAsistente="IUA2", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula3 = Vincula (asistentes_identificadorUnicoAsistente="IUA3", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula4 = Vincula (asistentes_identificadorUnicoAsistente="IUA4", eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula5 = Vincula (asistentes_identificadorUnicoAsistente="IUA1", eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    db.session.add (miVincula1);
    db.session.add (miVincula2);
    db.session.add (miVincula3);
    db.session.add (miVincula4);
    db.session.add (miVincula5);
    db.session.commit ();

    miDisponibleRobot1 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot2 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=102 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot3 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=103 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");

    miDisponibleRobot4 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");
    miDisponibleRobot5 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=103 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");
    miDisponibleRobot6 = DisponibleRobot (eventos_nombreDelEvento="simo1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=105 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");

    miDisponibleRobot7 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=105 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30");
    miDisponibleRobot8 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=106 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot9 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=101 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30");

    miDisponibleRobot10 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=107 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot11 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2025-02-01", fechaFinEnEvento="2025-02-28");
    miDisponibleRobot12 = DisponibleRobot (eventos_nombreDelEvento="simo1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=108 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");

    miDisponibleRobot13 = DisponibleRobot (eventos_nombreDelEvento="simo1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=109 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");
    miDisponibleRobot14 = DisponibleRobot (eventos_nombreDelEvento="simo1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=110 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot15 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=110 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");

    miDisponibleRobot16 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-10-01", fechaFinEnEvento="2024-10-30");
    miDisponibleRobot17 = DisponibleRobot (eventos_nombreDelEvento="simo1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=106 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");
    miDisponibleRobot18 = DisponibleRobot (eventos_nombreDelEvento="eurobot2042", eventos_fechaDeCreacionDelEvento="2024-11-27 11:19:48", eventos_lugarDondeSeCelebra="ifema2042", robots_idRobot=111 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");

    miDisponibleRobot19 = DisponibleRobot (eventos_nombreDelEvento="eurobot2042", eventos_fechaDeCreacionDelEvento="2024-11-27 11:19:48", eventos_lugarDondeSeCelebra="ifema2042", robots_idRobot=112 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot20 = DisponibleRobot (eventos_nombreDelEvento="eurobot2042", eventos_fechaDeCreacionDelEvento="2024-11-27 11:19:48", eventos_lugarDondeSeCelebra="ifema2042", robots_idRobot=113 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");


    db.session.add (miDisponibleRobot1);
    db.session.add (miDisponibleRobot2);
    db.session.add (miDisponibleRobot3);
    db.session.add (miDisponibleRobot4);
    db.session.add (miDisponibleRobot5);
    db.session.add (miDisponibleRobot6);
    db.session.add (miDisponibleRobot7);
    db.session.add (miDisponibleRobot8);
    db.session.add (miDisponibleRobot9);
    db.session.add (miDisponibleRobot10);
    db.session.add (miDisponibleRobot11);
    db.session.add (miDisponibleRobot12);
    db.session.add (miDisponibleRobot13);
    db.session.add (miDisponibleRobot14);
    db.session.add (miDisponibleRobot15);
    db.session.add (miDisponibleRobot16);
    db.session.add (miDisponibleRobot17);
    db.session.add (miDisponibleRobot18);
    db.session.add (miDisponibleRobot19);
    db.session.add (miDisponibleRobot20);
    db.session.commit ();



    return "<p> este es el index2 </p>"


######## endpoints funcionales. ######################################################################################################################################################################################################################

@app.before_request
def miFuncionAntesDeLaPeticion ():
    print  ("miFuncionAntesDeLaPeticion() --- este es el endpoint: ", request.endpoint); 
    miVariablePermitirAccesoSinCorreoElectronico = True;

    if (request.endpoint == 'index2') or (request.endpoint == None) or (request.endpoint == 'funcionAdministradorsignup') or (request.endpoint == 'funcion_aceptarRobot') or (request.endpoint == 'funcion_rechazarRobot') or (request.endpoint == 'funcion_registrarAsistente') or (request.endpoint == 'static') or (request.endpoint == 'funcionAdministradorLogin'):
        miVariablePermitirAccesoSinCorreoElectronico = False;

    # en el caso de que el correoElectronico no este en la sesion y ademas la URL que yo he puesto no sea de las permitidas, me voy al loggin.  
    if ('correoElectronico' not in session) and (miVariablePermitirAccesoSinCorreoElectronico == True):
        #print ("miFuncionAntesDeLaPeticion() --- en la sesion no esta el correo electronico, y el endpoint no es uno permitido, se va a redirigir al login. ");
        return redirect (url_for ('funcionAdministradorLogin'));

    #print("miFuncionAntesDeLaPeticion() --- request.view_args", request.view_args);
    # en caso de que el argumento del request  sea (entre otros) la clave ddel evento, es decir nombreDelEvento, fechaDeCreacionDelEvento y lugarDondeSeCelebra,  entonces voy a inicializar miDiccionarioEventoYasistentesDatos con esta clave. 
    # tambien con esa misma clave, voy a inicalizar miDiccionarioFechasPasoAEsPrivilegiado. 
    # Ademas voy a organizar los asistentes que van pasando a la cola de esPrivilegiado, es decir, voy a verificar si hay un primero en la cola, en el caso de que lo haya, voy a ver si su posiicionDeColaConFecha tiene una antigüedad
    # mayor a tres minutos, y si esto es cierto lo que hago es que a ese primero lo pongo como esPrivilegiado, pero claro viendo si ha pasado como minimo un minuto de que se haya pasado como privilegiado a otro asistente de ese mismo evento.

    if (request.view_args != None): 
        if (request.view_args.get('nombreDelEvento') != None) and (request.view_args.get('fechaDeCreacionDelEvento') != None) and (request.view_args.get('lugarDondeSeCelebra') != None):
            # aqui lo que voy a hacer es dejar como clave del evento, la concatenacion de nombreDelEvento, fechaDeCreacionDelEvento y lugarDondeSeCelebra del evento. 
            idEvento = request.view_args.get('nombreDelEvento') + request.view_args.get('fechaDeCreacionDelEvento') + request.view_args.get('lugarDondeSeCelebra');
            # con estos if, si no he inicializado los diccionarios, los inicializo, ya que estos son los que llevan el control de los turnos. 
            if (idEvento not in miDiccionarioEventoYasistentesDatos):
                miDiccionarioEventoYasistentesDatos[idEvento] = []; 
            if (idEvento not in miDiccionarioFechasPasoAEsPrivilegiado):
                miDiccionarioFechasPasoAEsPrivilegiado[idEvento] = datetime.now();  
            else:
                # de esta manera me aseguro que como maximo se va a pasar un asistente a la cola de privilegiados cada minuto, de esta manera no los meto a todos de golpe en esta nueva cola. 
                if (datetime.now() - miDiccionarioFechasPasoAEsPrivilegiado[idEvento] >= timedelta(minutes=1)): 
                    #en el caso de que tenga al menos un asistente ya en el evento. 
                    if (len (miDiccionarioEventoYasistentesDatos[idEvento]) > 0): 
                        miVariableFechaMasAntigua = datetime.now ();
                        miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = None;
                        for indiceNumerico, i in enumerate (miDiccionarioEventoYasistentesDatos[idEvento]):
                            # esto es para no tener en cuenta a las personas  que no tienen posicionDeColaConFecha, es decir cuento solamente con las que tienen fecha. Las que estan controlando un robot, o son privilegiadas no las cuento. 
                            # recordar que en indice 0 esta el identificadorUnicoAsistente, en el 1 esta posicionDeColaConFecha y en 2 esta esPrivilegiado (bool). 
                            if (i[1] != None):
                                if (i[1] < miVariableFechaMasAntigua):
                                    miVariableFechaMasAntigua = i[1];
                                     # de esta manera ya se en que posicion es donde tengo la fecha mas antigua. 
                                    miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = indiceNumerico;

                        # en caso de que la fecha actual menos la fecha extraida de la matriz (que tenia la posicionDeColaConFecha mas antigua),  la diferncia se mayor a 3 minutos.
                        if (datetime.now () - miVariableFechaMasAntigua >= timedelta (minutes = 3)):
                            # aqui lo que hago es que a ese asistente, lo paso como esPrivilegiad, dejandole su posicionDeColaConFecha en NULL, y su valor de esPrivilegiado en True. 
                            miDiccionarioEventoYasistentesDatos[idEvento][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][1] = None; 
                            miDiccionarioEventoYasistentesDatos[idEvento][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][2] = True; 
                            # aqui tomo la referencia del tiempo en el momento que he pasado un asistente a esPrivilegiado. 
                            miDiccionarioFechasPasoAEsPrivilegiado[idEvento] = datetime.now ();

    #este codigo es para que en el panel del home de cualquier administrador, actualize los valores de la cola, de tal forma que no tengo que poner segundos hilos de ejecucion para el paso de los asistentes a la cola de esPrivilegiado.
    if (request.endpoint == 'funcionAdministradorHome'):
        for clave, valor in miDiccionarioEventoYasistentesDatos.items():
            if (clave not in miDiccionarioFechasPasoAEsPrivilegiado): 
                miDiccionarioFechasPasoAEsPrivilegiado[clave] = datetime.now();
            else: 
                if (datetime.now() - miDiccionarioFechasPasoAEsPrivilegiado[clave] >= timedelta(minutes=1)): 
                    if (len (miDiccionarioEventoYasistentesDatos[clave]) > 0): 
                        miVariableFechaMasAntigua = datetime.now ();
                        miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = None;
                        for indiceNumerico, i in enumerate (miDiccionarioEventoYasistentesDatos[clave]):
                            if (i[1] != None): 
                                if (i[1] < miVariableFechaMasAntigua):
                                    miVariableFechaMasAntigua = i[1];
                                    miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo = indiceNumerico;
                        if (datetime.now () - miVariableFechaMasAntigua >= timedelta (minutes = 3)):
                            miDiccionarioEventoYasistentesDatos[clave][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][1] = None; 
                            miDiccionarioEventoYasistentesDatos[clave][miVariablePosicionDondeHeEncontradoAlAsistentenMasAntiguo][2] = True; 
                            miDiccionarioFechasPasoAEsPrivilegiado[clave] = datetime.now ();


@app.errorhandler (404)  # esto es para sacar el HTML que contiene el mensaje de error, para los casos en los que 
# la aplicacion caiga en algun error. 
def miPaginaNoEncntradaError (e):
	return render_template ("404.html"), 404; 

# este endpoint es necesario para la representacion de las imagenes en el HTML. Ya en la base dde datos la imagen se alamecena codificada, lo que hago aqui es decodificarla y darsela al HTML 
@app.route ('/capturarimagenrobot/<int:idRobot>')
def funcionCapturarImagenRobot (idRobot):
    miRobot = Robots.query.filter_by (_Robots__idRobot=idRobot).first();
    return send_file (BytesIO(miRobot.fotoDelRobot), mimetype='image/jpeg');

def crearApodoUnico ():
    miListaDeAnimales = ["TigreValiente", "DelfínSonriente", "BúhoSabio", "LeónCorajoso", "MariposaMágica", "PandaTierno", "ÁguilaLibre", "ZorroAstuto", "TortugaLenta", "LoboFeroz"];
    miApodoCreado = random.choice (miListaDeAnimales) + os.urandom(2).hex();
    #mientras ese apodo que me cabo de inventar, este en la BBDD, lo que hago es volver a generarlo.  Asi hasta que obtenga uno que no este en la tabla Asistentes, porque recordar que es clava candidata. 
    while (Asistentes.query.filter_by (_Asistentes__apodoAsistente = miApodoCreado).first() != None):
        miApodoCreado = random.choice (miListaDeAnimales) + os.urandom(2).hex();
    return miApodoCreado;

@app.route ("/generarcodgoqr/<url>")
def funcionGenerarCodigoQR (url):
    miQR = qrcode.QRCode (version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=7, border=2);
    miQR.add_data (url);
    miQR.make (fit=True);
    miImagenGenerada = miQR.make_image (fill_color="black", back_color="white");
    miImagenGenerada.save ("prueba.png");


######## endpoints Asistente. ########################################################################################################################################################################################################################

@app.route ("/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>") 
def funcion_registrarAsistente (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miEventos = Eventos.query.filter (Eventos._Eventos__nombreDelEvento == nombreDelEvento, Eventos._Eventos__fechaDeCreacionDelEvento == fechaDeCreacionDelEvento, Eventos._Eventos__lugarDondeSeCelebra == lugarDondeSeCelebra).first();
    if (miEventos == None):
        return "<p> funcion_registrarAsistente () --- error, el evento que se ha pasado por parametro, no existe. </p>";
    else:
        if (('token' in session) == False):
            session['token'] = os.urandom(24).hex(); 
            miAsistentes = Asistentes (identificadorUnicoAsistente = session['token'], apodoAsistente=crearApodoUnico(), eventos_nombreDelEvento=nombreDelEvento, eventos_fechaDeCreacionDelEvento= fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=lugarDondeSeCelebra);
            db.session.add (miAsistentes);
            db.session.commit ();
            miVincula = Vincula (asistentes_identificadorUnicoAsistente=session['token'], eventos_nombreDelEvento=nombreDelEvento, eventos_fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=lugarDondeSeCelebra, fechaAcceso=datetime.now(), fechaSalida=datetime.now() + timedelta(hours=6));
            db.session.add (miVincula);
            db.session.commit ();
        else: 
            # esta parte de aqui la hago porque puede haber clientes que almacenen su identificadorUnnicoAsistente, pero en otro momento se puede haber reseteado la aplicacion y la BBDD. 
            miAsistentes = Asistentes.query.filter_by (_Asistentes__identificadorUnicoAsistente= session['token']).first ();
            if (miAsistentes == None):
                miAsistentes = Asistentes (identificadorUnicoAsistente = session['token'], apodoAsistente=crearApodoUnico(), eventos_nombreDelEvento=nombreDelEvento, eventos_fechaDeCreacionDelEvento= fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=lugarDondeSeCelebra);
                db.session.add (miAsistentes);
                db.session.commit ();
                miVincula = Vincula (asistentes_identificadorUnicoAsistente=session['token'], eventos_nombreDelEvento=nombreDelEvento, eventos_fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=lugarDondeSeCelebra, fechaAcceso=datetime.now(), fechaSalida=datetime.now() + timedelta(hours=6));
                db.session.add (miVincula);
                db.session.commit ();
            else: 
                miVincula = Vincula.query.filter (Vincula.asistentes_identificadorUnicoAsistente == session['token'], Vincula.eventos_nombreDelEvento == nombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == fechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == lugarDondeSeCelebra).first();
                # en el caso de que haya token de sesion y este en la tabla Asistentes, pero no este vinculado a este evento (segun la BBDD), entonces lo vinculo a este otro evento nuevo, digo otro nuevo porque sí o sí este asistente para que exista, tiene que estar vinculado a un evento. 
                if (miVincula == None):
                    miVincula = Vincula (asistentes_identificadorUnicoAsistente=session['token'], eventos_nombreDelEvento=nombreDelEvento, eventos_fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=lugarDondeSeCelebra, fechaAcceso=datetime.now(), fechaSalida=datetime.now() + timedelta(hours=6));
                    db.session.add (miVincula);
                    db.session.commit ();

        idEvento = nombreDelEvento + fechaDeCreacionDelEvento + lugarDondeSeCelebra; 
        #aqui averiguo si ese token ya existe en el diccionario miDiccionarioEventoYasistentesDatos, para que de esta manera, no lo vuelva a meter. 
        miFilaDeDatosAsistente = [session['token'], datetime.now(), False];
        miMatrizComprobarAsistenteRegistrado = miDiccionarioEventoYasistentesDatos[idEvento];
        miVerdadComprobarAsistenteRegistrado = False;
        for miAsistenteDatos in miMatrizComprobarAsistenteRegistrado:
            # en el caso de quel asistente ya este registrado, lo que hago es quedarme con sus datos, no lo vuelvo a meter en el diccionario, por tanto por el lado del codigo un asistente puede estar unicamente 1 vez en un evento.
            if session['token'] == miAsistenteDatos[0]: 
                # en este punto yo ya sé que he contrado el asistente en la matriz, tengo que hacer ademas si ese asistente ya ha usado un robot, es decir, se le ha borrado la posicionDeColaConFecha, por lo tanto en el caso de que la tenga en NULL, lo que hago 
                # es establecerle la fecha actual.  Cuidado porque para que se le ponga la fecha, tiene que pasr ademas que ese asistente no sea privilegiado. 
                # en el caso de que la posicionDeColaConFeha sea NULL y no sea privilegiado, le vuelvo a establecer otra posicionDeColaConFecha. 
                if (miAsistenteDatos[1] == None) and (miAsistenteDatos[2] == False):
                    miAsistenteDatos[1] = datetime.now();
                miFilaDeDatosAsistente = miAsistenteDatos;
                miVerdadComprobarAsistenteRegistrado = True;
                break;
        # en el caso de que el asistenten no este en la matriz anterior del buble for, lo que hago es meterlo en el diccionario. 
        if (miVerdadComprobarAsistenteRegistrado == False): 
            miDiccionarioEventoYasistentesDatos[idEvento].append(miFilaDeDatosAsistente);

        # ahora lo que voy a hacer es ver cuantos robots a ese asistenten le voy a poder mostrar, es decir depuendiendo de su posición puede ver más o menos, por tanto voy a ver la cantidad de personas delante. 
        cantidadDePersonaDelante = 0;
         # en el caso de que ese asistente, no sea privilegiado, tengo que averiguar la cantidad de personas que tiiene delante.
        if (miFilaDeDatosAsistente[2] == False):
            fechaDeSolicitudDelRobot = miFilaDeDatosAsistente[1];
            # con este bucle for, veo la cantidad de personas que tengo delante. 
            for miAsistenteDatos in miDiccionarioEventoYasistentesDatos[idEvento]:
                # esto es para no tener en cuenta a las personas que ya estan controlando un robot, ya que si pasan a controlarlo, esta feche (posicionDeColaConFecha) se les borra. 
                if (miAsistenteDatos[1] != None):
                    if (miAsistenteDatos[1] < fechaDeSolicitudDelRobot):
                        cantidadDePersonaDelante = cantidadDePersonaDelante + 1;

        # ahora consigo los robots y ver que cantidad de robots rechazados ese token en ese evento tiene, para de esta manera no mostrarle los robot que  están rechazados. 
        miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==lugarDondeSeCelebra, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();
    
        # hay 3 pasos para conseguir un robot.
        # Paso1. esta es la parte que analiza la cantidad de robots que estan en servicio. 
        #aqui lo que hago es quitar elementos de la lista que acabo de obtener de la BBDD en funcion de si el roobot esta en servicio o no. 
        # con esto lo que hago es recorrer una copia de la lista, ya que la original la voy a modificcar: miListaDisponibleRobot[:]:
        for i in miListaDisponibleRobot[:]:
            miRobots = Robots.query.filter_by (_Robots__idRobot = i.robots_idRobot).first ();
            if (miRobots.disponible == False):
                miListaDisponibleRobot.remove (i);

        # paso2. de todos los robots que esten en servicio, voy a aliminar los que ya esten siendo usados. 
        for i in miListaDisponibleRobot[:]:
            miControla = Controla.query.filter (Controla.robots_idRobot == i.robots_idRobot, Controla.fechaTomaDelRobot < datetime.now(), Controla.fechaAbandonoDelRobot > datetime.now()).first ();
            # si este if se cumple, significa que  el robot está siendo utilizado. 
            if (miControla):
                miListaDisponibleRobot.remove (i); 

        #paso3. #aqui lo que hago es quitar elementos de la lista en funcion de las personas que tenga delante ese asistente.  
        for i in range (0 , cantidadDePersonaDelante): 
            if (miListaDisponibleRobot):
                miListaDisponibleRobot.pop(0);

        # sigo con la logica de los robots rechazados, deberia de coprobar prinero que todo si ese token en ese evento existe, en el caso que no, simplemente cojo el primer robot. 
        miVariabletokenDeSesionYevento = session ['token'] +"-" +str(idEvento);

        # en el caso de que la lista este vacia, es decir que no tenga ningun robot, entonces le devolvere un mensaje de que esta esperando por un robot. 
        if (not miListaDisponibleRobot):
            miListaRobots = [];
            miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==lugarDondeSeCelebra, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).all();
            for miDisponibleRobotObjeto in miListaDisponibleRobot: 
                miRobots = Robots.query.filter_by (_Robots__idRobot=miDisponibleRobotObjeto.robots_idRobot).first ();
                miListaRobots.append (miRobots);
            return (render_template("registrarasistente.html", miParametroMiEventoNombreDelEvento=miEventos.nombreDelEvento, miListaRobotsParametro=miListaRobots, miParametroIdentificadorUnicoAsistente=miAsistentes.identificadorUnicoAsistente, miParametroApodoAsistente=miAsistentes.apodoAsistente));
        else:
            # si he rechazado algun robot, voy a ver que otro robot le puedo ofrecer al asistente. 
            if (miVariabletokenDeSesionYevento in miDiccionarioGlobalTokensListaDeRobotsRechazados):
                miRobots = None;
                for miDisponibleRobotObjeto in miListaDisponibleRobot:
                    if (miDisponibleRobotObjeto.robots_idRobot not in miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento]):
                        miRobots = Robots.query.filter_by (_Robots__idRobot=miDisponibleRobotObjeto.robots_idRobot).first();
                        break;
                # en este caso si no he conseguido ningú robot, eso significa que he pasado todos, voy a olvodarme de todos los que he rechazado. 
                if (miRobots == None):
                    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento].clear ();
                    miRobots = Robots.query.filter_by (_Robots__idRobot=miListaDisponibleRobot[0].robots_idRobot).first();
                return render_template ("robotlisto.html", miRobotParametro=miRobots, miParametroMiEventoNombreDelEvento=miEventos.nombreDelEvento, miParametroFechaDeCreacionDelEvento=miEventos.fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra=miEventos.lugarDondeSeCelebra, miParametroIdentificadorUnicoAsistente=miAsistentes.identificadorUnicoAsistente, miParametroApodoAsistente=miAsistentes.apodoAsistente);
            else:
                miRobots = Robots.query.filter_by (_Robots__idRobot=miListaDisponibleRobot[0].robots_idRobot).first(); 
                return render_template ("robotlisto.html", miRobotParametro=miRobots, miParametroMiEventoNombreDelEvento=miEventos.nombreDelEvento, miParametroFechaDeCreacionDelEvento=miEventos.fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra=miEventos.lugarDondeSeCelebra, miParametroIdentificadorUnicoAsistente=miAsistentes.identificadorUnicoAsistente, miParametroApodoAsistente=miAsistentes.apodoAsistente);


@app.route ('/aceptarrobot/<int:idRobot>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>/<identificadorUnicoAsistente>')
def funcion_aceptarRobot (idRobot, nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, identificadorUnicoAsistente):

    #en el caso de que no ese asistente no exista en la BBDD, lo delvuelvo a funcion_registrarAsistente. 
    miAsistentes = Asistentes.query.filter_by (_Asistentes__identificadorUnicoAsistente = identificadorUnicoAsistente).first ();
    if (miAsistentes == None):
        return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra)); 

    miControla = Controla.query.filter (Controla.asistentes_identificadorUnicoAsistente == identificadorUnicoAsistente, Controla.fechaTomaDelRobot <=datetime.now(), Controla.fechaAbandonoDelRobot >= datetime.now()).first ();
    # en este momento el asistente esta controlando un robot. 
    if (miControla):
        # en este caso solisito el objeto Asistentes, ya que el es el que tiene los métodos para consultar eventos y consultar robots. 
        miRobots = miAsistentes.funcion_consultaRobot (miControla.robots_idRobot); 
        miEventos = miAsistentes.funcion_consultaEvento (miControla.robots_idRobot);
        return render_template ("robotmanejando.html", miRobotParametro=miRobots, miParametroMiEventoNombreDelEvento=miEventos.nombreDelEvento, miParametroIdentificadorUnicoAsistente=miAsistentes.identificadorUnicoAsistente, miParametroApodoAsistente=miAsistentes.apodoAsistente);
    else:
        # esta variable la uso psra extraer la posicionDeColaConFecha de del token en ese evento, que es lo que hago en el siguiente for.
        miPosicionDeColaConFecha = None; 
        # esta variable la uso para extraer el valor de si el asistente es o no privilegiado.  algo parecido a la variable: miPosicionDeColaConFecha
        miEsPrivilegiado = False; 
        idEvento = nombreDelEvento + fechaDeCreacionDelEvento + lugarDondeSeCelebra; 
        for indiceNumerico, i in enumerate(miDiccionarioEventoYasistentesDatos[idEvento]):
            # en el caso de que encuentre el identificadorUnicoAsistente dentro del indice cero de la lista que tiene [tokenDeSesion, posicionDeColaConFecha, esPrivilegiado], entonce me quedo con la posicionDeColaConFecha, para posteriormente ver si es null.
            if (identificadorUnicoAsistente == i[0]):
                miPosicionDeColaConFecha = i[1];
                miEsPrivilegiado = i[2];
                break; 
        # en el caso de que no tenga posicion de cola con fecha y no sea privilegiado, eso significa que en algun momento se le ha borrado, por lo tanto como no esta controlando un robot y tampoco tiene posicionDeColaConFecha, tengo que volver a 
        #funcion_registrarse, para que obtenga aqui  una nueva hora de solicitud de un robot. 
        if (miPosicionDeColaConFecha == None) and (miEsPrivilegiado == False):
            return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra));   
        else: 
            miControla = Controla.query.filter (Controla.robots_idRobot ==idRobot, Controla.fechaTomaDelRobot <=datetime.now(), Controla.fechaAbandonoDelRobot >= datetime.now()).first();
            # en el caso de que alguien se haya colado, y se ponga a controlar ese robot, lo que tengo que hacer es volver a funcion_registrarAsistente para conseguir otro robot. 
            if (miControla):
                return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra)); 
            else:
                miRobots = Robots.query.filter_by (_Robots__idRobot = idRobot).first ();
                # en el caso de que repentinamente el administrador haya borrado ese robot y no esta en la BBDD. 
                if (miRobots == None):
                    return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra)); 
                else: 
                    # aqui lo que hago es comprobar si el robot esta o no en servicio, en el caso de que no lo este, entonces lo mando a la  funcion_registrarAsistente para que consiga otro robot. 
                    if (miRobots.disponible == False):
                        return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra)); 
                    else:
                        miAsistentes.pasarAcontrolarRobot (identificadorUnicoAsistente, idRobot);
                        miRobots = miAsistentes.funcion_consultaRobot (idRobot); 
                        miEventos = miAsistentes.funcion_consultaEvento (idRobot);
                        # aqui lo que hago es, ese token buscarlo dentro de la matriz que proporciona el evento y el diccionario miDiccionarioEventoYasistentesDatos, cuando lo encuentre, a ese token el valor de indice 
                        # 1, lo establezco en null, para que posicionDeColaConFecha = None y el indice 2 lo establezco en False, para dejarlo como no privilegiado. 
                        for indiceNumerico, i in enumerate (miDiccionarioEventoYasistentesDatos[idEvento]):
                            # si encientro el token. 
                            if (identificadorUnicoAsistente == i[0]): 
                                # la posicion de cola con fecha la establezco en NULL. 
                                i[1] = None;
                                # tambien establezco que ya no es privilegiado. 
                                i[2] = False;
                                break;
                        # como ya es definitivo que paso a controlar un robot, lo que hago es que la lista del diccionario que almecena los robots que han sido rechazados, no tenga ningun elemento, para que cuando quiera elegir de nuevo un robot,
                        # (despues de que haya acabado el tiempo de utilizar uno o le haya expulsado un administradir) que no haya ningun problema. 
                        miVariabletokenDeSesionYevento = identificadorUnicoAsistente +"-" +str(idEvento);
                        # este if lo tengo porque unas veces el asistente no rechaza un robot, por lo tanto nunca se mete en este diccionario, entonces lo que estoy haciendo es ver primero si esta.
                        if (miVariabletokenDeSesionYevento in miDiccionarioGlobalTokensListaDeRobotsRechazados):
                            miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento].clear (); 
                        return (render_template ("robotmanejando.html", miRobotParametro=miRobots, miParametroMiEventoNombreDelEvento=miEventos.nombreDelEvento, miParametroIdentificadorUnicoAsistente=miAsistentes.identificadorUnicoAsistente, miParametroApodoAsistente=miAsistentes.apodoAsistente));


@app.route ('/rechazarrobot/<int:idRobot>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>/<identificadorUnicoAsistente>')
def funcion_rechazarRobot (idRobot, nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, identificadorUnicoAsistente):
    miAsistentes = Asistentes.query.filter_by (_Asistentes__identificadorUnicoAsistente = identificadorUnicoAsistente).first ();
    if (miAsistentes == None):
        return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra)); 

    # aqui lo que hago es dejar preparada la calve del diccionario miDiccionarioGlobalTokensListaDeRobotsRechazados para que su clave  sea el token y el idEvento, para que este elemento sea unico, lo que voy a dejar en el valor va a ser una lista de
    #idRobot para saber que estos son los que se han rechazado. 
    idEvento = nombreDelEvento + fechaDeCreacionDelEvento + lugarDondeSeCelebra; 
    miVariabletokenDeSesionYevento = session ['token'] +"-" +str(idEvento);

    # en el caso de que ese token con evento, no este en la clave del diccionrio, lo que hago es inicializarlo como lista, que recordar que ahi van a ir los robots que han sido rechazados.
    if (miVariabletokenDeSesionYevento not in miDiccionarioGlobalTokensListaDeRobotsRechazados): 
        miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento]  = []; 
    
    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYevento].append (idRobot);

    return redirect (url_for ('funcion_registrarAsistente', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra)); 



########################### endpoints Administrador con el robot. #####################################################################################################################################################################################
@app.route ("/administradorsignup", methods = ['GET', 'POST'])
def funcionAdministradorsignup ():
    miFormulario = formulario.FormularioAcceder (request.form);
    if (request.method == 'POST'):
        if (miFormulario.contrasena.data != miFormulario.confirmarContrasena.data):
            raise Exception ("administradorsignup --- las contarseñas no coinciden. ");
        miContrasenaHaseada = generate_password_hash (miFormulario.contrasena.data);
        miAdministradores = Administradores (correoElectronico=miFormulario.correoElectronico.data, contrasena=miContrasenaHaseada);
        db.session.add (miAdministradores);
        db.session.commit ();
        return redirect (url_for ('funcionAdministradorLogin'));

    return (render_template ("administradorsignup.html", miFormularioParametro=miFormulario));

@app.route ("/administradorlogin", methods = ['GET', 'POST'])
def funcionAdministradorLogin ():
    miFormulario = formulario.FormularioAcceder (request.form);
    miVariableUsuarioIncorrecto = False;
    miVariableContrasenaIncorrecta = False;
    if (request.method == 'POST'):
        miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=miFormulario.correoElectronico.data).first ();
        if (miAdministradores != None):
            if (miAdministradores.validarContrasena (miFormulario.contrasena.data)):
                session['correoElectronico'] = miAdministradores.correoElectronico;
                return redirect (url_for ('funcionAdministradorHome'));
            else:
                # en este caso la contraseña pasada, no coincide con el HASH, por lo tanto contraseña incorrecta. 
                miVariableContrasenaIncorrecta = True;
        else:
            #en este caso ni si quiera se ha encontrado a ese correo de administrador en la BBDD. 
            miVariableUsuarioIncorrecto = True;
            
    return (render_template("administradorlogin.html", miFormularioParametro = miFormulario, miParametroUsuarioIncorrecto = miVariableUsuarioIncorrecto, miParametroContrasenaIncorrecta = miVariableContrasenaIncorrecta));


@app.route ("/administradorcerrarsesion")
def funcionAdministradorCerrarSesion ():
    session.pop ('correoElectronico');
    return redirect (url_for ('funcionAdministradorLogin'));

@app.route('/administradorhome')   
def funcionAdministradorHome():
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miVariableCantidadDeEventosEnElSistema = len (miAdministradores.funcion_conseguirTodosLosEventos());
    miVariableCantidadRobotsEnElSistema = len (miAdministradores.funcion_conseguirTodosLosRobots ());
    miVariableCantidadAsistentensEnElSistema = 0;
    miListaAuxiiarAsistentesTotales = [];
    if (miDiccionarioEventoYasistentesDatos):  # en el caso de que el diccionario no este vacio. 
        for clave, valor in miDiccionarioEventoYasistentesDatos.items():
            for i in miDiccionarioEventoYasistentesDatos[clave]: # para cada lista de la matriz. 
                if i[0] not in miListaAuxiiarAsistentesTotales:  # si esa lista de indice cer, es decir si el tokenDeSesion,  no está en la lista miListaAuxiiarAsistentesTotales, entonces lo meto, de esta manera no tengo repetidos. 
                    miListaAuxiiarAsistentesTotales.append (i[0]);
    miVariableCantidadAsistentensEnElSistema = len (miListaAuxiiarAsistentesTotales);
    
    miVariableCantidadAsistentensEsperandoEnElSistema = 0;
    miListaAuxiliarAsistentesEsperando = [];
    if (miDiccionarioEventoYasistentesDatos):  # en el caso de que el diccionario no este vacio. 
        for clave, valor in miDiccionarioEventoYasistentesDatos.items():
            for i in miDiccionarioEventoYasistentesDatos[clave]: # para cada lista de la matriz. 
                if (i[0] not in miListaAuxiliarAsistentesEsperando) and (i[1] != None): 
                    miListaAuxiliarAsistentesEsperando.append (i[0]);
    miVariableCantidadAsistentensEsperandoEnElSistema = len (miListaAuxiliarAsistentesEsperando);

    miVariableCantidadDeEventosDelAdminstrador = len (miAdministradores.funcion_conseguirTodosLosEventosDeEseAdministrador());
    miVariableCantidadRobotsDelAdminstrador = len (miAdministradores.funcion_conseguirTodosLosRobots ());

    return (render_template ("administradorhome.html", parametroCantidadDeEventosEnElSistema=miVariableCantidadDeEventosEnElSistema, parametroCantidadDeRobotsEnElSistema=miVariableCantidadRobotsEnElSistema, 
    parametroCantidadAsistentesEnElSistema=miVariableCantidadAsistentensEnElSistema, parametroCantidadAsistentesEsperandoEnElSistema= miVariableCantidadAsistentensEsperandoEnElSistema, parametroCantidadDeEventosDelAdministrador=miVariableCantidadDeEventosDelAdminstrador));
   

@app.route ('/administradorpanelrobot/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
@app.route ('/administradorpanelrobot')
def funcionAdministradorPanelRobot (nombreDelEvento = None, fechaDeCreacionDelEvento = None, lugarDondeSeCelebra = None):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();

    miListaDeEventos = miAdministradores.funcion_conseguirTodosLosEventos ();
    miMostrarRobotsNingunEvento = False;

    if ((nombreDelEvento == None) and (fechaDeCreacionDelEvento == None) and (lugarDondeSeCelebra == None)):
        miListaRobots = miAdministradores.funcion_conseguirRobotsQueNoEstanEnNingunEvento();
        miMostrarRobotsNingunEvento = True;
    else:
        if ((nombreDelEvento == "todosLosRobots") and (fechaDeCreacionDelEvento == "todosLosRobots") and (lugarDondeSeCelebra=="todosLosRobots")):
            miListaRobots = miAdministradores.funcion_conseguirTodosLosRobots();
        else:
            miListaRobots = [];
            miListaDisponibleRobot = miAdministradores.funcion_conseguirDisponibleRobotPorEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
            for miDisponibleRobotObjeto in miListaDisponibleRobot:
                miRobot = miAdministradores.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robots_idRobot);
                if (miRobot not in miListaRobots): # aqui sólo añado los robots que no se repiten, por eso compruebo primero si esta.
                    miListaRobots.append (miRobot);

    return render_template ("administradorpanelrobot.html", miListaRobotsParametro=miListaRobots, miListaDeEventosParametro=miListaDeEventos, miParametroMostrarRobotsNingunEvento=miMostrarRobotsNingunEvento);


@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>')
def funcionAdministradorPanelRobotBorrar (idRobot, nombreDelEvento=None, fechaDeCreacionDelEvento=None, lugarDondeSeCelebra=None):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    if (miAdministradores.funcion_verSiPuedoBorrarRobot (idRobot) == False):
        raise Exception ("administradorpaneleventoborrar.html --- ese administrador, no puede eliminar ese robot.");

    miAdministradores.funcion_borrarRobot (idRobot);

    if ((nombreDelEvento == None) and (fechaDeCreacionDelEvento == None) and (lugarDondeSeCelebra == None)):
        return redirect (url_for ('funcionAdministradorPanelRobot'));
    else:
        return redirect (url_for ('funcionAdministradorModificarRobotsEvento', nombreDelEvento = nombreDelEvento, fechaDeCreacionDelEvento = fechaDeCreacionDelEvento, lugarDondeSeCelebra = lugarDondeSeCelebra));

@app.route ('/administradorcrearrobot', methods = ['GET', 'POST'])
def funcionAdministradorCrearRobot ():
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCreaRobot (request.form);
    # ya que administradorcrearrobot.html lo utilizo en crear robot, modificar roboot y en modificar robot cuando estoy dentro del evento, el idEvento es una variable que se utiliza a la hora de renderizar, es decir
    # ver que elementos HTML son los que se van a mostrar, por lo tanto en esta linea voy a poner un evento NULL.  
    nombreDelEvento = None;
    fechaDeCreacionDelEvento = None;
    lugarDondeSeCelebra = None;

    if (request.method == 'POST') and (miFormulario.validate ()): 
        fotoRecibidaDelFormulario = request.files['fotoDelRobot'];
        binarioDeFoto = fotoRecibidaDelFormulario.read();
        # de esta forma detrmino si hay o no hay foto, ya que en el caso de que el peso de la foto sea 0, eso significa que no se ha adjuntado la foto.
        if (len (binarioDeFoto) == 0): 
            # de esta forma en el caso de que la foto no se haya insertado, entonces a la BBDD le paso el valor de NULL. 
            binarioDeFoto = None;
        else:
            #En esta parte voy a poner la validación del documento que se sube a la página web, la foto debe de pesar como maximo 10MB, ademas los formatos validdos son 
            #Jpg, jpeg y png. 
            miExpresionRegularParaJPG = r".+\.jpg$";
            miExpresionRegularParaJPEG = r".+\.jpeg$";
            miExpresionRegularParaPNG = r".+\.png$";
            miVerdadEsJPG = bool(re.match (miExpresionRegularParaJPG, fotoRecibidaDelFormulario.filename));
            miVerdadEsJPEG = bool(re.match (miExpresionRegularParaJPEG, fotoRecibidaDelFormulario.filename));
            miVerdadEsPNG = bool(re.match (miExpresionRegularParaPNG, fotoRecibidaDelFormulario.filename));
            if (miVerdadEsJPG == False) and (miVerdadEsJPEG == False) and (miVerdadEsPNG == False):
                raise Exception ("administradorcrearrobot.html --- la extesión del archivo no es valida, las extensiones permitidas son .jpg .jpeg y .png");
            #else:
                #print ("funcionAdministradorCrearRobot()--- este es el tamaño en KB:   ", len(binarioDeFoto)/1024);
        
        miAdministradores.funcion_crearRobot (miFormulario.macAddressDelRobot.data, miFormulario.nombreDelRobot.data, binarioDeFoto, miFormulario.descripcionDelRobot.data);
        return redirect(url_for('funcionAdministradorPanelRobot'));

    return render_template ('administradorcrearrobot.html', miFormularioParametro = miFormulario, miParametroAccionHtml = "crear", miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento= fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra= lugarDondeSeCelebra);



# en esta parte dejo la posibilidad de que este endpoint no reciba el evento, ya que puedde ser que se modifique un robot desde el panel robot, el cual muestra todos los robots que no estan en ningun evento, y recordar que en esta parte cualquier administrador
#puede modificar un robot, por lo tanto despues de modificarlo la pantalla de muestra no tiene porque ser la de gestion de robots en evento, si no que puede ser que se quede en la misma pudiendo modificar mas robots. 
@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>', methods = ['GET', 'POST'])
@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobotModificar (idRobot, nombreDelEvento = None, fechaDeCreacionDelEvento = None, lugarDondeSeCelebra = None):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCreaRobot (request.form);

    if (request.method == 'POST'):
        if (miFormulario.validate()):
            fotoRecibidaDelFormulario = request.files['fotoDelRobot'];
            binarioDeFoto = fotoRecibidaDelFormulario.read();
            if (len(binarioDeFoto) == 0):
                binarioDeFoto = None;
            miAdministradores.funcion_modificarRobot (idRobot, miFormulario.macAddressDelRobot.data, miFormulario.nombreDelRobot.data, binarioDeFoto, miFormulario.descripcionDelRobot.data);

            if ((nombreDelEvento == None) and (fechaDeCreacionDelEvento == None) and (lugarDondeSeCelebra == None)):
                return redirect(url_for('funcionAdministradorPanelRobot')); 
            else:   
                return redirect (url_for ('funcionAdministradorModificarRobotsEvento', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra));
        else:
            # en el caso de que no se valide el formulario, lo que hago es que devuelvo el formulario con los datos que se acaban de rellenar por el request.form y en este ya está almacenado el error. 
            return render_template ("administradorcrearrobot.html", miFormularioParametro=miFormulario, miParametroAccionHtml="modificar", miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento= fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra= lugarDondeSeCelebra);
    else:
        # esto es para comprobar si se esta edtando un robot que no esta asociado a ningun evento. 
        if (miAdministradores.funcion_verSiUnRobotEstaEnAlMenosUnEvento (idRobot)):
            # dado que un adinistrador que conoce el idRobot de un robot que no se le muestra, el puede poner en la URL que lo va a modificar, con este IF yo comppruebo si ese administrador lo va a utilizar en algun momento. En el caso de que no, no le dejo modificar.
            if (miAdministradores.funcion_verSiEseRobotEsDeEseAdministrador (idRobot) == False):
                raise Exception ("administradorpaneleventoborrar.html --- ese administrador, no utiliza, ni va a utilizar ese robot, por lo tanto no lo va a modificar.");
            else:
                #en el caso de que un administrador vea un robot, sabiendo que esta en la tabla de disponible, pero que ademas ese robot lo estan utilizando actualmente, entonces no se le va a mostrar la opcion de modificar, pero lo que pasa es que si el pone en la URL
                # a este robot, entonecs sí que lo puede modificar, por lo tanto hago este if que vuelve a comprobar si ese administrador lo puede o no modificar, en el caso de que no pueda, le mando un error. 
                if (miAdministradores.funcion_verSiPuedoModificarRobot (idRobot) == False):
                    raise Exception ("administradorpaneleventoborrar.html --- ese administrador, no puede modificcar ese robot, ya que otro adminsitrador lo esta usando actualmente. ");
        miRobot = miAdministradores.funcion_conseguirRobotPorIdRobot (idRobot);
        miFormulario = formulario.FormularioCreaRobot(obj=miRobot);
        return render_template ("administradorcrearrobot.html", miFormularioParametro=miFormulario, miParametroAccionHtml="modificar", miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento= fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra= lugarDondeSeCelebra);





########################### endpoints Administrador con los eventos #####################################################################################################################################################################################

@app.route ('/administradorpanelevento/<int:miVerdadErrorDeEventoInexistente>')
@app.route ('/administradorpanelevento')
def funcionAdministradorPanelEvento (miVerdadErrorDeEventoInexistente = 0):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miListaEventos = miAdministradores.funcion_conseguirTodosLosEventosDeEseAdministrador ();
    return render_template ("administradorpanelevento.html", miListaEventosParametro=miListaEventos, miParametroVerdadErrorDeEventoInexistente=miVerdadErrorDeEventoInexistente);
    




@app.route ('/administradorpaneleventoborrar/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
def funcionAdministradorPanelEventoBorrar (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    if (miAdministradores.funcion_verSiEseEventoEsDeEseAdministrador  (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra)):
        miAdministradores.funcion_borrarEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
        return redirect (url_for ('funcionAdministradorPanelEvento'));
    else:
        raise Exception ("administradorpaneleventoborrar.html --- para ese adminstrador, ese evento no existe")


@app.route ('/administradorcrearevento', methods = ['GET', 'POST'])
def funcionAdministradorCrearEvento ():
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCrearEvento (request.form);
    
    if (request.method == 'POST'):
        miAdministradores.funcion_crearEvento (miFormulario.nombreDelEvento.data, miFormulario.lugarDondeSeCelebra.data, miFormulario.calle.data, miFormulario.numero.data, miFormulario.codigoPostal.data);
        return redirect (url_for ('funcionAdministradorPanelEvento'));

    return render_template ("administradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "crear");



@app.route ('/administradormodificardatosevento/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
def funcionAdministradorModificarDatosEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCrearEvento (request.form);

    if (request.method == 'POST'):
        miAdministradores.funcion_modificarDatosDelEvento (nombreDelEvento, miFormulario.fechaDeCreacionDelEvento.data, lugarDondeSeCelebra, miFormulario.nombreDelEvento.data,  miFormulario.lugarDondeSeCelebra.data, miFormulario.calle.data, miFormulario.numero.data, miFormulario.codigoPostal.data);
        return redirect(url_for('funcionAdministradorPanelEvento'));

    if (miAdministradores.funcion_verSiEseEventoEsDeEseAdministrador  (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra)):
        miEventos = miAdministradores.funcion_conseguirEventoPorClavePrimaria (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
        miFormulario = formulario.FormularioCrearEvento (obj=miEventos);
        return render_template ("administradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar");
    else:
        return redirect(url_for('funcionAdministradorPanelEvento', miVerdadErrorDeEventoInexistente=1));

@app.route ('/administradormodificarrobotsevento/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
def funcionAdministradorModificarRobotsEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();

    if (request.method == 'POST'):
        if ('nameformulariomodificar' in request.form):
            miAdministradores.funcion_modificarRobotDelEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, request.form.get('robots_idRobot'), request.form.get('fechaComienzoEnEventoAntigua'), request.form.get('fechaFinEnEventoAntigua'), 
                                                               request.form.get('fechaComienzoEnEvento'), request.form.get('fechaFinEnEvento'));
        else:
            if ("nameformulariosumarrobot" in request.form):
                miIdRobotRecibido = request.form.get('idRobot');
                miFechaComienzoEnEventoRecibido = request.form.get ('fechaComienzoEnEvento');
                miHoraComienzoEnEventoRecibido = request.form.get ('fechaComienzoEnEventoHora');
                # esto de sumar un espacion en blanco, es para separar el dia mes año, de la hora y el minuto, para que de esta forma este fecha completa entre en la BBDD. 
                if (miFechaComienzoEnEventoRecibido != "" and miHoraComienzoEnEventoRecibido != ""):
                    miFechaComienzoEnEventoRecibido += " ";
                    miFechaComienzoEnEventoRecibido += miHoraComienzoEnEventoRecibido;

                miFechaFinEnEventoRecibido = request.form.get ('fechaFinEnEvento');
                miHoraFinEnEventoRecibido = request.form.get ('fechaFinEnEventoHora');
                if (miFechaFinEnEventoRecibido != "" and miHoraFinEnEventoRecibido != ""):
                    miFechaFinEnEventoRecibido += " ";
                    miFechaFinEnEventoRecibido += miHoraFinEnEventoRecibido;
                miAdministradores.funcion_sumarRobotAlEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, miIdRobotRecibido, miFechaComienzoEnEventoRecibido, miFechaFinEnEventoRecibido);
            else:
                if ("nameformularioeliminar" in request.form):
                    miAdministradores.funcion_eliminarRobotDelEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, request.form.get('robots_idRobot'), request.form.get('fechaComienzoEnEventoAntigua'), request.form.get('fechaFinEnEventoAntigua'));
                else:
                    raise Exception ("administradormodificarrobotsevento.htmml --- formulario invalido.");
    
    if (miAdministradores.funcion_verSiEseEventoEsDeEseAdministrador (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra)):
        miDiccionarioRobotsActualmenteEstanEnEvento = {};
        miListaDisponibleRobot = miAdministradores.funcion_conseguirDisponibleRobotPorEventoYporEstarContempladaLaFechaDelSistema (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
        #  este for me vale para rellenar los robots del evento. tabla1.
        for miDisponibleRobotObjeto in miListaDisponibleRobot: 
            miRobot = miAdministradores.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robots_idRobot);
            if (miRobot not in miDiccionarioRobotsActualmenteEstanEnEvento):
                # de esta manera inicializo el vector. 
                miDiccionarioRobotsActualmenteEstanEnEvento[miRobot] = []; 
            miDiccionarioRobotsActualmenteEstanEnEvento[miRobot].append (miDisponibleRobotObjeto);  
        #este for es para rellenar en el diccionario que almacena los robots de la tabla 1, par que el diccionario tenga tambien de cada uno de los robots en conocimiento de si debe mostrar los botones de borrar, modificar y enServicio. 
        for clave in miDiccionarioRobotsActualmenteEstanEnEvento:
            miVariablePuedoeliminar = miAdministradores.funcion_verSiPuedoBorrarRobot (clave.idRobot);
            miVariableQueBotonEnServicioEs = not(clave.disponible);
            miDiccionarioRobotsActualmenteEstanEnEvento[clave] = {"subclaveListas":miDiccionarioRobotsActualmenteEstanEnEvento[clave], "subclavePuedoeliminar": miVariablePuedoeliminar, "subclaveQueBotonEnServicioEs": miVariableQueBotonEnServicioEs};
    
        # esto me vale para rellenar la tabla2. 
        miDiccionarioRobotsActualmenteNoEstanEnEvento = {};
        miListaDisponibleRobot = miAdministradores.funcion_conseguirDisponibleRobotPorEventoYporNoEstarContempladaLaFechaDelSistema (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
        for miDisponibleRobotObjeto in miListaDisponibleRobot: 
            miRobot = miAdministradores.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robots_idRobot);
            if (miRobot not in miDiccionarioRobotsActualmenteNoEstanEnEvento):
                miDiccionarioRobotsActualmenteNoEstanEnEvento[miRobot] = [];
            miDiccionarioRobotsActualmenteNoEstanEnEvento[miRobot].append (miDisponibleRobotObjeto);  
        for clave in miDiccionarioRobotsActualmenteNoEstanEnEvento:
            miVariablePuedoeliminar = miAdministradores.funcion_verSiPuedoBorrarRobot (clave.idRobot);
            miVariablePuedoModificar = miAdministradores.funcion_verSiPuedoModificarRobot (clave.idRobot);
            miVariableQueBotonEnServicioEs = not(clave.disponible);
            miDiccionarioRobotsActualmenteNoEstanEnEvento[clave] = {"subclaveListas":miDiccionarioRobotsActualmenteNoEstanEnEvento[clave], "subclavePuedoModificar": miVariablePuedoModificar, "subclavePuedoeliminar": miVariablePuedoeliminar, "subclaveQueBotonEnServicioEs": miVariableQueBotonEnServicioEs};

        # este for me vale para rellenar los formularios de los robots que no estan en ese evento. tabla 3. (la de abajo del todo).
        miListaDeSumarRobot = [];
        for miRobotObjeto in miAdministradores.funcion_conseguirTodosLosRobotsQueNoSonDeEseEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra): 
            miListaDeSumarRobot.append ([miRobotObjeto.idRobot, miRobotObjeto.macAddressDelRobot]);
        return render_template ("administradormodificarrobotsevento.html", miDiccionarioRobotsActualmenteEstanEnEvetoParametro=miDiccionarioRobotsActualmenteEstanEnEvento, miDiccionarioRobotsActualmenteNoEstanEnEvetoParametro=miDiccionarioRobotsActualmenteNoEstanEnEvento,
                                 miListaDeSumarRobotParametro=miListaDeSumarRobot, miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento=fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra=lugarDondeSeCelebra);
    else:
        return redirect(url_for('funcionAdministradorPanelEvento', miVerdadErrorDeEventoInexistente=1))


@app.route ('/adminstradorpanelrobotponerservicio/<int:idRobot>/<int:robotEnServicio>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
def funcionAdministradorPanelRobotPonerServicio (idRobot, robotEnServicio, nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra): 
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first(); 
    # este if lo pongo, ya que en el caso de que otro administrador conozca el idRoot y el evento en el que etá, puede modificar el servicio del robot, por lo tanto para evitar eseo, copruebo que es el dueño del robot
    #el que esta modificando el servicio del robot. 
    if (miAdministradores.funcion_verSiPuedoModificarRobot (idRobot) == False):
        raise Exception ("adminstradorpanelrobotponerservicio  --- ese administrador no puede modificar el servicio de ese robot, ya que actualmente la hora de trabajo de este robot no se corresponde con ningun evento de este administrador. ");
    miAdministradores.funcion_activarOdesactivarRobot (idRobot, robotEnServicio);
    return redirect (url_for ('funcionAdministradorModificarRobotsEvento', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra));




########################### endpoints Administrador con las cuentas #####################################################################################################################################################################################
@app.route ('/administradorpaneladministradorgestioncuentas')
def funcionAdministradorGestioncuentas ():
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first();
    miListaAdministradores = miAdministradores.funcion_conseguirTodasLasCuentasMenosLaInstanciada ();
    miDiccionarioAdministradores = {};
    miListaDeEventos = [];
    for i in miListaAdministradores:
        miListaDeEventos = miAdministradores.funcion_conseguirTodosLosEventosPorCorreoElectronico (i.correoElectronico);
        miDiccionarioAdministradores[i.correoElectronico] = miListaDeEventos;
    return render_template ("administradorpanelgestioncuentas.html", miParametroDiccionarioAdministradores = miDiccionarioAdministradores);

@app.route ('/administradorborrarcuentaadministrador/<correoelectronico>')
def funcionAdministradorBorrarCuentaAdministrador (correoelectronico):
    miAdministradores = Administradores.query.filter_by (_Administradores__correoElectronico=session['correoElectronico']).first ();
    miAdministradores.funcion_borrarCuentaAdministrador (correoelectronico);
    return redirect (url_for ('funcionAdministradorGestioncuentas'));

######## Configuración de Flask.  ##################################################################################################################################################################################################################

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



