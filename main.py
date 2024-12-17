# el request,  me vale para recibir parámetros por a URL. 
# el redirect me vale para redirigir a los usuarios a otra pagina de mi aplicacion. 
# el url_for genera una url para una de las funciones que tengo en este main.py. 
# el session es para el menajo de las sessiones de los usuarios en la pagina web. . 
from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import CSRFProtect
# esta librería me vale para generar u CSRF tokem que le enviaré a los cliete de la API, para que posteriormente ellos me lo devuelva y de esta forma se pueda llevar a cabo la comunicación entre Androir y la API. 
from flask_wtf.csrf import generate_csrf
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
# esto es para codificar las imágenes en base64, que es la forma de enviarle las fotos a Kodular. 
import base64
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

# esta es la librería PILLOW con el que hago la compresión de la imágenes.
# La calse Image me vale para convertir a Imagen los Bytes que saco de la base de datos. 
# La clase ImageOps la uso para
from PIL import Image, ImageOps

# esto es para enviar los correos electrónicos.
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)
app.config.from_object (DevelopmentConfig);
csrf = CSRFProtect ();
mail = Mail (app);

# este diccionario lo voy a utilizar para almacenar como clave al identificadorUnicoAsistente y como valor, un bool el cual determina si ese asistente esta manejando o no un robot.  
# esto se utiliza (por ejemplo, hay más casos) para que cuando un asistente este en el endpoint de aceptarRobot y se le  haya acababo el tiempo de uso del robot, este valor esté en 
#true, para que de esta forma se le vuelva a ese asistente a la parte en la que se le muestra otro robot disponible , para  que despues acepte o rechace ese nuevo robot propuesto, si
# esto no lo hago, lo que pasa es que ese asistente que maneja este robot, en el momento que acceda al endpoint y no se haya registrado si es una solicitud de robot nueva o una antigua, 
# se va a meter a ese asistente en el robot otra vez, y a lo mejor ese asistente no quiere manejar ese robot otros cinco minutos. 
miDiccionarioAsistentesYestadoControlandoRobot = {}

# en este diccionario la clave va a ser el token con el evento , para saber que asistenten en que evento hay rechazado un robot, para que de esta forma no se le muestre uno que el haya rechazado en el evento. 
miDiccionarioGlobalTokensListaDeRobotsRechazados = {}

# en este diccionario la clave es el correo electronico del administrador que ha solicitado cambiar la contraseñamm y el valor es el token (48 carecteres hexagesimal) que se le envían al correo 
# que solicitó cambiar la contraseña, para que cuando el admininstrador acceda a su correo, que haga clic en la url que envía 
miDiccionarioCorreoElectroncoYtokenRestablecerContrasena = {};

miVariableGlobalURL = "http://localhost:5000/demostracionesroboticas/"; 



@app.route ("/index")
def index ():
    return "<p>Hello, World! Demostraciones Robóticas.</p>"
    

@app.route ("/index2")
def index2 ():
    contrasnaHasheda = generate_password_hash ("james")
    miAdmin1 = Administradores (_correoElectronico="jhon@gmail.com", _contrasena=contrasnaHasheda);
    miAdmin2 = Administradores (_correoElectronico="ana@gmail.com", _contrasena=contrasnaHasheda);
    miAdmin3 = Administradores (_correoElectronico="alberto@gmail.com", _contrasena=contrasnaHasheda);

    db.session.add (miAdmin1);
    db.session.add (miAdmin2);
    db.session.add (miAdmin3);
    db.session.commit ();

    miEvento1 = Eventos (_nombreDelEvento="aula1", _fechaDeCreacionDelEvento='2024-10-01', _lugarDondeSeCelebra="ifema1", _codigoQR="miQR1", _administradores_correoElectronico="jhon@gmail.com");
    miEvento2 = Eventos (_nombreDelEvento="puertas abiertas1", _fechaDeCreacionDelEvento='2024-10-01', _lugarDondeSeCelebra="alcala", _codigoQR="miQR2", _administradores_correoElectronico="jhon@gmail.com");
    miEvento3 = Eventos (_nombreDelEvento="eurobot2042", _fechaDeCreacionDelEvento='2024-11-27 11:19:48', _lugarDondeSeCelebra="ifema2042", _codigoQR="eurobot20422024-11-27T11:19:48ifema2042", _administradores_correoElectronico="jhon@gmail.com");
    miEvento4 = Eventos (_nombreDelEvento="simo2025", _fechaDeCreacionDelEvento='2024-10-01', _lugarDondeSeCelebra="torrejon", _codigoQR="simo20252024-10-01torrejon", _administradores_correoElectronico="ana@gmail.com");
    miEvento5 = Eventos (_nombreDelEvento="mobile week 2025", _fechaDeCreacionDelEvento='2024-10-01', _lugarDondeSeCelebra="torrejon", _codigoQR="mlileWeek2025-10-01torrejon", _administradores_correoElectronico="ana@gmail.com");
    miEvento6 = Eventos (_nombreDelEvento="aula2", _fechaDeCreacionDelEvento='2024-11-27 11:19:48', _lugarDondeSeCelebra="ifema2042", _codigoQR="miQR3", _administradores_correoElectronico="jhon@gmail.com");
    miEvento7 = Eventos (_nombreDelEvento="aula3", _fechaDeCreacionDelEvento='2024-10-01', _lugarDondeSeCelebra="ibiza hotel", _codigoQR="miQR4", _administradores_correoElectronico="ana@gmail.com");
    db.session.add (miEvento1);
    db.session.add (miEvento2);
    db.session.add (miEvento3);
    db.session.add (miEvento4);
    db.session.add (miEvento5);
    db.session.add (miEvento6);
    db.session.add (miEvento7);
    db.session.commit ();



    miAsistente1 = Asistentes (_identificadorUnicoAsistente="IUA1", _apodoAsistente="apodo1");
    miAsistente2 = Asistentes (_identificadorUnicoAsistente="IUA2", _apodoAsistente="apodo2");
    miAsistente3 = Asistentes (_identificadorUnicoAsistente="IUA3", _apodoAsistente="apodo3");
    miAsistente4 = Asistentes (_identificadorUnicoAsistente="IUA4", _apodoAsistente="apodo4");
    db.session.add (miAsistente1);
    db.session.add (miAsistente2);
    db.session.add (miAsistente3);
    db.session.add (miAsistente4);
    db.session.commit  ();

    miRobot1 = Robots (_idRobot=101, _macAddressDelRobot="00:00:00:00:00:00", _nombreDelRobot="robot1", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot2 = Robots (_idRobot=102, _macAddressDelRobot="11:11:11:11:11:11", _nombreDelRobot="robot2", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot3 = Robots (_idRobot=103, _macAddressDelRobot="22:22:22:22:22:22", _nombreDelRobot="robot3", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot4 = Robots (_idRobot=104, _macAddressDelRobot="33:33:33:33:33:33", _nombreDelRobot="robot4", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot5 = Robots (_idRobot=105, _macAddressDelRobot="44:44:44:44:44:44", _nombreDelRobot="robot5", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot6 = Robots (_idRobot=106, _macAddressDelRobot="55:55:55:55:55:55", _nombreDelRobot="robot6", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot7 = Robots (_idRobot=107, _macAddressDelRobot="66:66:66:66:66:66", _nombreDelRobot="robot7", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot8 = Robots (_idRobot=108, _macAddressDelRobot="77:77:77:77:77:77", _nombreDelRobot="robot8", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot9 = Robots (_idRobot=109, _macAddressDelRobot="88:88:88:88:88:88", _nombreDelRobot="robot9", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot10 = Robots (_idRobot=110, _macAddressDelRobot="99:99:99:99:99:99", _nombreDelRobot="robot10", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot11 = Robots (_idRobot=111, _macAddressDelRobot="AA:AA:AA:AA:AA:AA", _nombreDelRobot="robot11", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot12 = Robots (_idRobot=112, _macAddressDelRobot="BB:BB:BB:BB:BB:BB", _nombreDelRobot="robot12", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot13 = Robots (_idRobot=113, _macAddressDelRobot="CC:CC:CC:CC:CC:CC", _nombreDelRobot="robot13", _fotoDelRobot=None, _descripcionDelRobot=None);

    miRobot14 = Robots (_idRobot=114, _macAddressDelRobot="AB:AB:AB:AB:AB:AB", _nombreDelRobot="robot14", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot15 = Robots (_idRobot=115, _macAddressDelRobot="AC:AC:AC:AC:AC:AC", _nombreDelRobot="robot15", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot16 = Robots (_idRobot=116, _macAddressDelRobot="AD:AD:AD:AD:AD:AD", _nombreDelRobot="amigobot16", _fotoDelRobot=None, _descripcionDelRobot=None);
    miRobot17 = Robots (_idRobot=117, _macAddressDelRobot="AE:AE:AE:AE:AE:AE", _nombreDelRobot="amigobot17", _fotoDelRobot=None, _descripcionDelRobot=None);
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
    db.session.add (miRobot14);
    db.session.add (miRobot15);
    db.session.add (miRobot16);
    db.session.add (miRobot17);
    db.session.commit ();

    miVincula1 = Vincula (asistentes_identificadorUnicoAsistente="IUA1", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-12-01", fechaSalida="2024-12-30");
    miVincula2 = Vincula (asistentes_identificadorUnicoAsistente="IUA2", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-12-01", fechaSalida="2024-12-30");
    miVincula3 = Vincula (asistentes_identificadorUnicoAsistente="IUA3", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-12-01", fechaSalida="2024-12-30");
    miVincula4 = Vincula (asistentes_identificadorUnicoAsistente="IUA4", eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", fechaAcceso="2024-12-01", fechaSalida="2024-12-30");
    miVincula5 = Vincula (asistentes_identificadorUnicoAsistente="IUA1", eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", fechaAcceso="2024-12-01", fechaSalida="2024-12-30");
    db.session.add (miVincula1);
    db.session.add (miVincula2);
    db.session.add (miVincula3);
    db.session.add (miVincula4);
    db.session.add (miVincula5);
    db.session.commit ();

    miDisponibleRobot1 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);
    miDisponibleRobot2 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=102 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);
    miDisponibleRobot3 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=103 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);

    miDisponibleRobot4 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=False);
    miDisponibleRobot5 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=103 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=True);
    miDisponibleRobot6 = DisponibleRobot (eventos_nombreDelEvento="simo2025", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=105 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=True);

    miDisponibleRobot7 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=105 , fechaComienzoEnEvento="2025-02-01", fechaFinEnEvento="2025-02-28 23:23:23", disponible=True);
    miDisponibleRobot8 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=106 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=False);
    miDisponibleRobot9 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=101 , fechaComienzoEnEvento="2025-02-01", fechaFinEnEvento="2025-02-28 23:23:23", disponible=True);

    miDisponibleRobot10 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=107 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);
    miDisponibleRobot11 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2025-03-01", fechaFinEnEvento="2025-03-28 23:23:23", disponible=False);
    miDisponibleRobot12 = DisponibleRobot (eventos_nombreDelEvento="simo2025", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=108 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=True);

    miDisponibleRobot13 = DisponibleRobot (eventos_nombreDelEvento="simo2025", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=109 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=True);
    miDisponibleRobot14 = DisponibleRobot (eventos_nombreDelEvento="simo2025", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=110 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);
    miDisponibleRobot15 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=110 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=True);

    miDisponibleRobot16 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30 23:23:23", disponible=True);
    miDisponibleRobot17 = DisponibleRobot (eventos_nombreDelEvento="simo2025", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=106 , fechaComienzoEnEvento="2025-01-01", fechaFinEnEvento="2025-01-30 23:23:23", disponible=True);
    miDisponibleRobot18 = DisponibleRobot (eventos_nombreDelEvento="eurobot2042", eventos_fechaDeCreacionDelEvento="2024-11-27 11:19:48", eventos_lugarDondeSeCelebra="ifema2042", robots_idRobot=111 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);

    miDisponibleRobot19 = DisponibleRobot (eventos_nombreDelEvento="eurobot2042", eventos_fechaDeCreacionDelEvento="2024-11-27 11:19:48", eventos_lugarDondeSeCelebra="ifema2042", robots_idRobot=112 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);
    miDisponibleRobot20 = DisponibleRobot (eventos_nombreDelEvento="eurobot2042", eventos_fechaDeCreacionDelEvento="2024-11-27 11:19:48", eventos_lugarDondeSeCelebra="ifema2042", robots_idRobot=113 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30 23:23:23", disponible=True);
    miDisponibleRobot20 = DisponibleRobot (eventos_nombreDelEvento="mobile week 2025", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="torrejon", robots_idRobot=113 , fechaComienzoEnEvento="2025-03-01", fechaFinEnEvento="2025-12-30 23:23:23", disponible=True);


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

    if (request.endpoint == 'index2') or (request.endpoint == None) or (request.endpoint == 'funcionAdministradorsignup') or (request.endpoint == 'funcion_aceptarRobot') or (request.endpoint == 'funcion_rechazarRobot') or (request.endpoint == 'funcion_registrarAsistente') or (request.endpoint ==
         'static') or (request.endpoint == 'funcionAdministradorLogin') or (request.endpoint == 'funcionErrorClienteServidor') or (request.endpoint == 'demostracionesroboticas'):
        miVariablePermitirAccesoSinCorreoElectronico = False;

    # en el caso de que el correoElectronico no este en la sesion y ademas la URL que yo he puesto no sea de las permitidas, me voy al loggin.  
    if ('correoElectronico' not in session) and (miVariablePermitirAccesoSinCorreoElectronico == True):
        return redirect (url_for ('funcionAdministradorLogin'));



@app.errorhandler (404)  # esto es para sacar el HTML que contiene el mensaje de error, para los casos en los que la aplicacion caiga en algun error. 
def miPaginaNoEncntradaError (e):
	return render_template ("error.html", parametroMensajeError = e), 404; 

@app.route ('/errorclienteservidor/<mensajeerror>')
def funcionErrorClienteServidor (mensajeerror = None):
    return render_template ("error.html", parametroMensajeError = mensajeerror);


# este endpoint es necesario para la representacion de las imagenes en el HTML. Ya en la base dde datos la imagen se alamecena codificada, lo que hago aqui es decodificarla y darsela al HTML 
@app.route ('/capturarimagenrobot/<int:idRobot>')
def funcionCapturarImagenRobot (idRobot):
    miRobot = Robots.query.filter_by (_idRobot=idRobot).first();
    return send_file (BytesIO(miRobot._fotoDelRobot), mimetype='image/jpeg');

def crearApodoUnico ():
    miListaDeAnimales = ["TigreValiente", "DelfínSonriente", "BúhoSabio", "LeónCorajoso", "MariposaMágica", "PandaTierno", "ÁguilaLibre", "ZorroAstuto", "TortugaLenta", "LoboFeroz"];
    miApodoCreado = random.choice (miListaDeAnimales)  +"#"  + os.urandom(2).hex();
    #mientras ese apodo que me cabo de inventar, este en la BBDD, lo que hago es volver a generarlo.  Asi hasta que obtenga uno que no este en la tabla Asistentes, porque recordar que es clava candidata. 
    while (Asistentes.query.filter_by (_apodoAsistente = miApodoCreado).first() != None):
        miApodoCreado = random.choice (miListaDeAnimales) + os.urandom(2).hex();
    return miApodoCreado;

@app.route ("/generarcodgoqr/<url>")
@app.route ("/generarcodgoqr/<url>/<correoelectronico>")
def funcionGenerarCodigoQR (url, correoelectronico = None):
    if (correoelectronico != None):
        miCodigoQR = qrcode.make (miVariableGlobalURL + url +"/" +correoelectronico);
    else:
        miCodigoQR = qrcode.make (miVariableGlobalURL + url);

    # Con esto se crea una lista de bits para almacenar el codigo QR que genera la librería qrcode, para después envieárselo al cliente y no que el servidor se queda con la imagen. 
    # Es como un buffer que se prepara para el almacenamiento de archivos. 
    miPreparacionImagen  = BytesIO();
    miCodigoQR.save(miPreparacionImagen, format='PNG');

    # Esto es obligatorio hacerlo por que cuando se escribe en el objeto BytesIO, hay un puntero que indice el principio del archivo y una vez que se ha escrito, este ppuntero indica
    # el principio del archivo, al final de este, por lo tanto hay que volver este puntero al principio del objeto para saber en donde empieza. 
    miPreparacionImagen.seek(0);
    # esto as_attachment lo que indica es que se obtendrá como un descargable. 
    return send_file(miPreparacionImagen, mimetype='image/png', as_attachment=True, download_name=miVariableGlobalURL + url + ".png");


######## endpoints Asistente. ########################################################################################################################################################################################################################
@app.route ("/demostracionesroboticas/<codigoQR>") 
@app.route ("/demostracionesroboticas/<codigoQR>/<correoelectronico>") 
def funcion_registrarAsistente (codigoQR, correoelectronico = None):
    miEventos = Eventos.query.filter (Eventos._codigoQR == codigoQR).first();
    if (miEventos == None):
        miRespuestaJson = {"miParametroMiEventoNombreDelEvento":None, "miParametroApodoUsuario":None, "miParametroEstado":"error404, evento no encontrado","miParametroIdRobot": None, "miParametroMac" : None,
                            "miParametroCorreoElectronicoDelAdministrador" : None, "miParametroCodigoQR": None, "miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
        return jsonify(miRespuestaJson), 404;
    else:
        if (('token' in session) == False):
            session['token'] = os.urandom(24).hex(); 
            try:
                miAsistentes = Asistentes (_identificadorUnicoAsistente = session['token'], _apodoAsistente=crearApodoUnico());
                db.session.add (miAsistentes);
                miVincula = Vincula (asistentes_identificadorUnicoAsistente=session['token'], eventos_nombreDelEvento=miEventos._nombreDelEvento, eventos_fechaDeCreacionDelEvento=miEventos._fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=miEventos._lugarDondeSeCelebra, fechaAcceso=datetime.now(), fechaSalida=datetime.now() + timedelta(hours=1));
                db.session.add (miVincula);
                db.session.commit ();
            except Exception as e:
                db.session.rollback();
                miRespuestaJson = {"miParametroMiEventoNombreDelEvento":None, "miParametroApodoUsuario":None, "miParametroEstado":"error500, error en la bae de datos","miParametroIdRobot": None, "miParametroMac" : None, "miParametroCorreoElectronicoDelAdministrador" : None, "miParametroCodigoQR": None, "miParametroFotoDelRobot":None,"miParametroCSRFtoken":generate_csrf()};
                return jsonify(miRespuestaJson), 500;
                #return redirect (url_for ('funcionErrorClienteServidor', mensajeerror=e));  
        else: 
            # esta parte de aqui la hago porque puede haber clientes que almacenen su identificadorUnnicoAsistente, pero en otro momento se puede haber reseteado la aplicacion y la BBDD. 
            miAsistentes = Asistentes.query.filter_by (_identificadorUnicoAsistente= session['token']).first ();
            if (miAsistentes == None):
                try:
                    miAsistentes = Asistentes (_identificadorUnicoAsistente = session['token'], _apodoAsistente=crearApodoUnico());
                    db.session.add (miAsistentes);
                    db.session.commit ();
                    miVincula = Vincula (asistentes_identificadorUnicoAsistente=session['token'], eventos_nombreDelEvento=miEventos._nombreDelEvento, eventos_fechaDeCreacionDelEvento=miEventos._fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=miEventos._lugarDondeSeCelebra, fechaAcceso=datetime.now(), fechaSalida=datetime.now() + timedelta(hours=1));
                    db.session.add (miVincula);
                    db.session.commit ();
                except Exception as e:
                    db.session.rollback();
                    miRespuestaJson = {"miParametroMiEventoNombreDelEvento":None, "miParametroApodoUsuario":None, "miParametroEstado":"error500, error en la base de datos","miParametroIdRobot": None, "miParametroMac" : None, "miParametroCorreoElectronicoDelAdministrador" : None, "miParametroCodigoQR": None,"miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
                    return jsonify(miRespuestaJson), 500;
                    #return redirect (url_for ('funcionErrorClienteServidor', mensajeerror=e));  
            else: 
                miVincula = Vincula.query.filter (Vincula.asistentes_identificadorUnicoAsistente == session['token'], Vincula.eventos_nombreDelEvento == miEventos._nombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == miEventos._fechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == miEventos._lugarDondeSeCelebra).first();
                # en el caso de que haya token de sesion y este en la tabla Asistentes, pero no este vinculado a este evento (segun la BBDD), entonces lo vinculo a este otro evento nuevo, digo otro nuevo porque sí o sí este asistente para que exista, tiene que estar vinculado a un evento. Pongo esto 
                # porque me puedo llegar a imaginar que la aplicacion de Kodular funciona de la siguiente manera: Un asistente maneja robots un día, y quizás una semana después aunque la aplicación se haya caido, la aplicación cliente de Kodular guarda el sesion token para esa URL, y por lo tanto el 
                # asistente sí tiene token de sesion, está en la tabla asistente, pero con este nuevo evento, no está en la tabla vincula. 
                if (miVincula == None):
                    miVincula = Vincula (asistentes_identificadorUnicoAsistente=session['token'], eventos_nombreDelEvento=miEventos._nombreDelEvento, eventos_fechaDeCreacionDelEvento=miEventos._fechaDeCreacionDelEvento, eventos_lugarDondeSeCelebra=miEventos._lugarDondeSeCelebra, fechaAcceso=datetime.now(), fechaSalida=datetime.now() + timedelta(hours=6));
                    db.session.add (miVincula);
                    db.session.commit ();
        
        # Ya que el cliente no tienen ninga accion para decir que ha cerreado la aplcaicion, sí se registra alguna acción suya despues de la hora de fechaAcceso, entonces su hora de salida será la actual más una hora.  Esto nos vale para estimar su hora de salida. 
        if (datetime.now() > miVincula.fechaSalida):
            miVincula.fechaSalida = datetime.now() + timedelta (hours=1);
            db.session.commit ();

        # en el caso de que el token no esté inicializado en miDiccionarioAsistentesYestadoControlandoRobot, entonces lo inicializo. 
        if (session['token'] not in miDiccionarioAsistentesYestadoControlandoRobot):
            miDiccionarioAsistentesYestadoControlandoRobot[session['token']] = False;
        else:
            # solemente en el caso de que sea True, entonces lo voy a establecer  en false, ya que me imagino que por lo que sea Kodular puede estar haciendo muchas peticiones a este endpoint y para optimizar lo que hago es comprobar si es True, de esta forma hago menos escrituras en el codigo. 
            if (miDiccionarioAsistentesYestadoControlandoRobot[session['token']] == True):
                miDiccionarioAsistentesYestadoControlandoRobot[session['token']] = False;

        # ahora consigo los robots a los que podría pasar a controlar.  En esta caso hay dos posibilidades, que la peticion de un robot venga por un chaval o un padre de la calle o de algún administrador de las demostraciones robóticas. Al administrador le voy a mostrar hasta los que no estén en servicio. 
        miVariableCorreoElectronicoAdministrador = None;
        if (correoelectronico != None):
            miAdministradores = Administradores.query.filter_by (_correoElectronico = correoelectronico).first ();
            if (miAdministradores):
                miVariableCorreoElectronicoAdministrador = miAdministradores._correoElectronico;
                miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==miEventos._nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==miEventos._fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==miEventos._lugarDondeSeCelebra, 
                                                                       DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= (datetime.now()+timedelta(minutes=5))).all();
            else:
                # esto es para el caso de que en la URL se haya pasado un correoElectronico inventado y no exista en la base de datos. 
                miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==miEventos._nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==miEventos._fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==miEventos._lugarDondeSeCelebra, 
                                                                       DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= (datetime.now()+timedelta(minutes=5)), DisponibleRobot.disponible == True).all();
        else:
            miListaDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.eventos_nombreDelEvento==miEventos._nombreDelEvento, DisponibleRobot.eventos_fechaDeCreacionDelEvento==miEventos._fechaDeCreacionDelEvento, DisponibleRobot.eventos_lugarDondeSeCelebra==miEventos._lugarDondeSeCelebra, 
                                                               DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= (datetime.now()+timedelta(minutes=5)), DisponibleRobot.disponible == True).all();
        # este valor lo establezcoon en 5 minutos ya que este es el tiempo máximo que se va a esperar por el prócimo robot. En el caso de que el tiempo máxmo de espera por un robot sea más de 5 minutos, eso significa que no hay robots disponibles para 
        # eese asistente y por lo tanto no debería esperar por un robot, si no que se le debería avisar que no hay robots disponibles para asistentes. 
        miVariableTiempoParaElProximoRobot = timedelta (minutes=5);
        # este es el caso en el que en la aplicación no hay robots en los que pasar a controlar, no porque estén todos ocupados, si no porque el administrador no ha puesto ninguno disponible para los asistentes. 
        if (len (miListaDisponibleRobot) == 0):
            miRespuestaJson = {"miParametroMiEventoNombreDelEvento":miEventos._nombreDelEvento, "miParametroApodoUsuario":miAsistentes._apodoAsistente, "miParametroEstado":"Las demostraciones robóticas no están disponibles, no hay robots para manejar","miParametroIdRobot": None, "miParametroMac" : None, "miParametroCorreoElectronicoDelAdministrador" : miVariableCorreoElectronicoAdministrador, "miParametroCodigoQR": codigoQR, "miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
            return jsonify(miRespuestaJson), 200;
        else:
            # de todos los robots que he conseguido de la tabla disponibleRobot, voy a eliminar los que ya esten siendo usados. 
            for i in miListaDisponibleRobot[:]:
                miControla = Controla.query.filter (Controla.robots_idRobot == i.robots_idRobot, Controla.fechaTomaDelRobot < datetime.now(), Controla.fechaAbandonoDelRobot > datetime.now()).first ();
                # si este if se cumple, significa que  el robot está siendo utilizado. 
                if (miControla):
                    miListaDisponibleRobot.remove (i); 
                    miVariableAuxiliarTiempoParaElProximoRobot =  miControla.fechaAbandonoDelRobot - datetime.now();
                    if (miVariableTiempoParaElProximoRobot > miVariableAuxiliarTiempoParaElProximoRobot):
                        miVariableTiempoParaElProximoRobot = miVariableAuxiliarTiempoParaElProximoRobot;
                    

        # en el caso de que la lista este vacia, es decir que no tenga ningun robot, entonces le devolvere un mensaje de que esta esperando por un robot. 
        if (not miListaDisponibleRobot):
            miRespuestaJson = {"miParametroMiEventoNombreDelEvento":miEventos._nombreDelEvento, "miParametroApodoUsuario":miAsistentes._apodoAsistente, "miParametroEstado":"Esperando por un robot, tiempo de espera para el proximo: "+str(miVariableTiempoParaElProximoRobot),"miParametroIdRobot": None, "miParametroMac" : None, "miParametroCorreoElectronicoDelAdministrador" : miVariableCorreoElectronicoAdministrador, "miParametroCodigoQR": codigoQR, "miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
            return jsonify(miRespuestaJson), 200;
            #return (render_template("registrarasistente.html", miParametroMiEventoNombreDelEvento=miEventos._nombreDelEvento, miParametroApodoUsuario=miAsistentes._apodoAsistente, miParametroEstado="Esperando", miParametroIdRobot = None, miParametroMac = None, miParametroCorreoElectronicoDelAdministrador = miVariableCorreoElectronicoAdministrador, miParametroCodigoQR = codigoQR));
        else:
            # por ultimo lo que hago es la lógica de los robots rechazados. 
            miVariabletokenDeSesionYeventoQR = session ['token'] +"-" +codigoQR;
            # si he rechazado algun robot, voy a ver que otro robot le puedo ofrecer al asistente. 
            if (miVariabletokenDeSesionYeventoQR in miDiccionarioGlobalTokensListaDeRobotsRechazados):
                miRobots = None;
                for miDisponibleRobotObjeto in miListaDisponibleRobot:
                    if (miDisponibleRobotObjeto.robots_idRobot not in miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYeventoQR]):
                        miRobots = Robots.query.filter_by (_idRobot=miDisponibleRobotObjeto.robots_idRobot).first();
                        break;
                # en este caso si no he conseguido ningún robot, eso significa que he pasado todos, voy a olvidarme de todos los que he rechazado. 
                if (miRobots == None):
                    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYeventoQR].clear ();
                    miRobots = Robots.query.filter_by (_idRobot=miListaDisponibleRobot[0].robots_idRobot).first();
                miFotoDelRobotCodificadaString = None;
                if (miRobots._fotoDelRobot != None):
                    miFotoDelRobotCodificadaBase64 = base64.b64encode(miRobots._fotoDelRobot);
                    miFotoDelRobotCodificadaString = miFotoDelRobotCodificadaBase64.decode("utf-8"); 
                miRespuestaJson = {"miParametroMiEventoNombreDelEvento":miEventos._nombreDelEvento, "miParametroApodoUsuario":miAsistentes._apodoAsistente, "miParametroEstado":"Robot Listo","miParametroIdRobot": miRobots._idRobot, "miParametroMac" : miRobots._macAddressDelRobot, "miParametroCorreoElectronicoDelAdministrador" : miVariableCorreoElectronicoAdministrador, "miParametroCodigoQR": codigoQR,
                                    "miParametroFotoDelRobot":miFotoDelRobotCodificadaString, "miParametroCSRFtoken":generate_csrf()};
                return jsonify(miRespuestaJson), 200;
                #return render_template ("robotlisto.html", miParametroMiEventoNombreDelEvento=miEventos._nombreDelEvento, miParametroApodoUsuario=miAsistentes._apodoAsistente, miParametroEstado="Robot Listo", miParametroIdRobot=miRobots._idRobot, miParametroMac = miRobots._macAddressDelRobot, miParametroCorreoElectronicoDelAdministrador = miVariableCorreoElectronicoAdministrador, miParametroCodigoQR=codigoQR);
           # en este caso que ese token con ese evento, no está en el miDiccionarioGlobalTokensListaDeRobotsRechazados  entonces eso significa que ese asistente, nunca ha rechazado un robot, por tanto le propongo el primer robot que encuentre. 
            else:
                miRobots = Robots.query.filter_by (_idRobot=miListaDisponibleRobot[0].robots_idRobot).first(); 
                miFotoDelRobotCodificadaString = None;
                if (miRobots._fotoDelRobot != None):
                    miFotoDelRobotCodificadaBase64 = base64.b64encode(miRobots._fotoDelRobot);
                    miFotoDelRobotCodificadaString = miFotoDelRobotCodificadaBase64.decode("utf-8");               
                miRespuestaJson = {"miParametroMiEventoNombreDelEvento":miEventos._nombreDelEvento, "miParametroApodoUsuario":miAsistentes._apodoAsistente, "miParametroEstado":"Robot Listo","miParametroIdRobot": miRobots._idRobot, "miParametroMac" : miRobots._macAddressDelRobot, "miParametroCorreoElectronicoDelAdministrador" : miVariableCorreoElectronicoAdministrador, "miParametroCodigoQR": codigoQR,
                                    "miParametroFotoDelRobot":miFotoDelRobotCodificadaString, "miParametroCSRFtoken":generate_csrf()};
                return jsonify(miRespuestaJson), 200;
                #return render_template ("robotlisto.html", miParametroMiEventoNombreDelEvento=miEventos._nombreDelEvento, miParametroApodoUsuario=miAsistentes._apodoAsistente, miParametroEstado="Robot Listo", miParametroIdRobot=miRobots._idRobot, miParametroMac = miRobots._macAddressDelRobot, miParametroCorreoElectronicoDelAdministrador = miVariableCorreoElectronicoAdministrador, miParametroCodigoQR=codigoQR);


# Estas lineas eran la que usaba pasa las pruebas, para simular que un navegador cualquiera era el que hacia las peticiones del robot. 
#@app.route ('/aceptarrobot/<int:idRobot>/<codigoQR>')
#@app.route ('/aceptarrobot/<int:idRobot>/<codigoQR>/<correoelectronico>')
#def funcion_aceptarRobot (idRobot, codigoQR, correoelectronico = None):

# de esta forma sólo se reciben mensajes por el POST. 
@app.route ('/aceptarrobot', methods = ['POST'])
def funcion_aceptarRobot ():
    miJsonRecibido = request.get_json ();
    codigoQR = miJsonRecibido['miParametroCodigoQR'];
    correoelectronico = miJsonRecibido ['miParametroCorreoElectronicoDelAdministrador'];
    idRobot = miJsonRecibido['miParametroIdRobot'];

    miEventos = Eventos.query.filter (Eventos._codigoQR == codigoQR).first();
    if (miEventos == None):
        miRespuestaJson = {"miParametroMiEventoNombreDelEvento":None, "miParametroApodoUsuario":None, "miParametroEstado":"error404, evento no encontrado","miParametroIdRobot": None, "miParametroMac" : None, "miParametroCorreoElectronicoDelAdministrador" : None, "miParametroCodigoQR": None, "miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
        return jsonify(miRespuestaJson), 404;
        #return "<p> funcion_registrarAsistente () --- error, el evento que se ha pasado por parametro, no existe. </p>";
    else:
        miVariableCorreoElectronicoAdministrador = None;
        miAdministradores = None;
        if (correoelectronico != None):
            miAdministradores = Administradores.query.filter_by (_correoElectronico = correoelectronico).first ();
            if (miAdministradores):
                miVariableCorreoElectronicoAdministrador = miAdministradores._correoElectronico;
                
        if (('token' in session) == False):
            return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
        else:
            #en el caso de que no ese asistente no exista en la BBDD, lo delvuelvo a funcion_registrarAsistente. 
            miAsistentes = Asistentes.query.filter_by (_identificadorUnicoAsistente = session['token']).first ();
            if (miAsistentes == None):
                return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
            else:
                miVincula = Vincula.query.filter (Vincula.asistentes_identificadorUnicoAsistente == session['token'], Vincula.eventos_nombreDelEvento == miEventos._nombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == miEventos._fechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == miEventos._lugarDondeSeCelebra).first();
                if (miVincula == None):
                    return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 

        if (datetime.now() > miVincula.fechaSalida):
            miVincula.fechaSalida = datetime.now() + timedelta (hours=1);
            db.session.commit ();

        miControla = Controla.query.filter (Controla.asistentes_identificadorUnicoAsistente == miAsistentes._identificadorUnicoAsistente, Controla.fechaTomaDelRobot <=datetime.now(), Controla.fechaAbandonoDelRobot >= datetime.now()).first ();
        # en este momento el asistente esta controlando un robot. 
        if (miControla):
            # en este caso solicito el objeto Asistentes, ya que el es el que tiene los métodos para consultar eventos y consultar robots. 
            miRobots = miAsistentes.funcion_consultaRobot (miControla.robots_idRobot); 
            miEventos = miAsistentes.funcion_consultaEvento (miControla.robots_idRobot);
            miRespuestaJson = {"miParametroMiEventoNombreDelEvento":miEventos._nombreDelEvento, "miParametroApodoUsuario":miAsistentes._apodoAsistente, "miParametroEstado":"Robot manejando","miParametroIdRobot": miRobots._idRobot, "miParametroMac" : miRobots._macAddressDelRobot, "miParametroCorreoElectronicoDelAdministrador" : miVariableCorreoElectronicoAdministrador, "miParametroCodigoQR": codigoQR,
                                "miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
            return jsonify(miRespuestaJson), 200;
            #return render_template ("robotmanejando.html",  miParametroMiEventoNombreDelEvento=miEventos._nombreDelEvento, miParametroApodoUsuario=miAsistentes._apodoAsistente, miParametroEstado="Robot manejando", miParametroIdRobot=miRobots._idRobot, miParametroMac = miRobots._macAddressDelRobot, miParametroCorreoElectronicoDelAdministrador = miVariableCorreoElectronicoAdministrador, miParametroCodigoQR=codigoQR);
        else:
            # de esta forma prevengo el fallo de que si la aplicacion se cae, que a kodeular no le de error, ya que cuando la aplcacion empieza a ejecutarse, ningun diccionario esta inicializado. 
            if (miAsistentes._identificadorUnicoAsistente not in miDiccionarioAsistentesYestadoControlandoRobot):
                return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
            else:
                if (miDiccionarioAsistentesYestadoControlandoRobot[miAsistentes._identificadorUnicoAsistente] == True):
                    return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
                else:
                    miControla = Controla.query.filter (Controla.robots_idRobot ==idRobot, Controla.fechaTomaDelRobot <=datetime.now(), Controla.fechaAbandonoDelRobot >= datetime.now()).first();
                    # en el caso de que alguien se haya colado, y se ponga a controlar ese robot, lo que tengo que hacer es volver a funcion_registrarAsistente para conseguir otro robot. 
                    if (miControla):
                        return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
                    else:
                        miRobots = miAsistentes.funcion_consultaRobot (idRobot); 
                        # en el caso de que repentinamente el administrador haya borrado ese robot y no esta en la BBDD. 
                        if (miRobots == None):
                            return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador));     
                        else: 
                            # aqui lo que hago es comprobar si el robot esta o no en servicio, en el caso de que no lo este, entonces lo mando a la  funcion_registrarAsistente para que consiga otro robot. En el caso de que seas un administrador sigo el codigo para controlar un robot que no está en servicio. 
                            miDisponibleRobot = DisponibleRobot.query.filter (DisponibleRobot.robots_idRobot == idRobot, DisponibleRobot.fechaComienzoEnEvento <= datetime.now(), DisponibleRobot.fechaFinEnEvento >= datetime.now()).first ();
                            if (miDisponibleRobot.disponible == False) and (miAdministradores == None):
                                return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = None)); 
                            else:
                                miAsistentes.pasarAcontrolarRobot (miAsistentes._identificadorUnicoAsistente, idRobot);
                                miEventos = miAsistentes.funcion_consultaEvento (idRobot);
                                miDiccionarioAsistentesYestadoControlandoRobot[miAsistentes._identificadorUnicoAsistente] = True;
                                # como ya es definitivo que paso a controlar un robot, lo que hago es que la lista del diccionario que almecena los robots que han sido rechazados, no tenga ningun elemento, para que cuando quiera elegir de nuevo un robot,
                                # (despues de que haya acabado el tiempo de utilizar uno o le haya expulsado un administradir) que no haya ningun problema. 
                                miVariabletokenDeSesionYeventoQR = miAsistentes._identificadorUnicoAsistente +"-" +codigoQR;
                                # este if lo tengo porque unas veces el asistente no rechaza un robot, por lo tanto nunca se mete en este diccionario, entonces lo que estoy haciendo es ver primero si esta.
                                if (miVariabletokenDeSesionYeventoQR in miDiccionarioGlobalTokensListaDeRobotsRechazados):
                                    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYeventoQR].clear (); 
                                miRespuestaJson = {"miParametroMiEventoNombreDelEvento":miEventos._nombreDelEvento, "miParametroApodoUsuario":miAsistentes._apodoAsistente, "miParametroEstado":"Robot manejando","miParametroIdRobot": miRobots._idRobot, "miParametroMac" : miRobots._macAddressDelRobot, "miParametroCorreoElectronicoDelAdministrador" : miVariableCorreoElectronicoAdministrador, "miParametroCodigoQR": codigoQR,
                                                    "miParametroFotoDelRobot":None,"miParametroCSRFtoken":generate_csrf()};
                                return jsonify(miRespuestaJson), 200;
                                #return render_template ("robotmanejando.html",  miParametroMiEventoNombreDelEvento=miEventos._nombreDelEvento, miParametroApodoUsuario=miAsistentes._apodoAsistente, miParametroEstado="Robot manejando", miParametroIdRobot=miRobots._idRobot, miParametroMac = miRobots._macAddressDelRobot, miParametroCorreoElectronicoDelAdministrador = miVariableCorreoElectronicoAdministrador, miParametroCodigoQR=codigoQR);

#@app.route ('/rechazarrobot/<int:idRobot>/<codigoQR>')
#@app.route ('/rechazarrobot/<int:idRobot>/<codigoQR>/<correoelectronico>')
#def funcion_rechazarRobot (idRobot, codigoQR, correoelectronico = None):
@app.route ('/rechazarrobot', methods = ['POST'])
def funcion_rechazarRobot ():
    miJsonRecibido = request.get_json ();
    codigoQR = miJsonRecibido['miParametroCodigoQR'];
    correoelectronico = miJsonRecibido ['miParametroCorreoElectronicoDelAdministrador'];
    idRobot = miJsonRecibido['miParametroIdRobot'];


    miEventos = Eventos.query.filter (Eventos._codigoQR == codigoQR).first();
    if (miEventos == None):
        miRespuestaJson = {"miParametroMiEventoNombreDelEvento":None, "miParametroApodoUsuario":None, "miParametroEstado":"error404, evento no encontrado","miParametroIdRobot": None, "miParametroMac" : None, "miParametroCorreoElectronicoDelAdministrador" : None, "miParametroCodigoQR": None, "miParametroFotoDelRobot":None, "miParametroCSRFtoken":generate_csrf()};
        return jsonify(miRespuestaJson), 404;   
        #return "<p> funcion_registrarAsistente () --- error, el evento que se ha pasado por parametro, no existe. </p>";
    else:
        miVariableCorreoElectronicoAdministrador = None;
        if (correoelectronico != None):
            miAdministradores = Administradores.query.filter_by (_correoElectronico = correoelectronico).first ();
            if (miAdministradores):
                miVariableCorreoElectronicoAdministrador = miAdministradores._correoElectronico;

        if (('token' in session) == False):
            return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
        else:
            miAsistentes = Asistentes.query.filter_by (_identificadorUnicoAsistente = session['token']).first ();
            if (miAsistentes == None):
                return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 
            else:
                miVincula = Vincula.query.filter (Vincula.asistentes_identificadorUnicoAsistente == session['token'], Vincula.eventos_nombreDelEvento == miEventos._nombreDelEvento, Vincula.eventos_fechaDeCreacionDelEvento == miEventos._fechaDeCreacionDelEvento, Vincula.eventos_lugarDondeSeCelebra == miEventos._lugarDondeSeCelebra).first();
                if (miVincula == None):
                    return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 

    if (datetime.now() > miVincula.fechaSalida):
        miVincula.fechaSalida = datetime.now() + timedelta (hours=1);
        db.session.commit ();

    # aqui lo que hago es dejar preparada la calve del diccionario miDiccionarioGlobalTokensListaDeRobotsRechazados para que su clave  sea el token y el codigoQR, para que este elemento sea unico, lo que voy a dejar en el valor va a ser una lista de
    #idRobot para saber que estos son los que se han rechazado. 
    miVariabletokenDeSesionYeventoQR = miAsistentes._identificadorUnicoAsistente +"-" +codigoQR;

    # en el caso de que ese token con evento, no este en la clave del diccionrio, lo que hago es inicializarlo como lista, que recordar que ahi van a ir los robots que han sido rechazados.
    if (miVariabletokenDeSesionYeventoQR not in miDiccionarioGlobalTokensListaDeRobotsRechazados): 
        miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYeventoQR]  = []; 
    
    miDiccionarioGlobalTokensListaDeRobotsRechazados[miVariabletokenDeSesionYeventoQR].append (idRobot);
    return redirect (url_for ('funcion_registrarAsistente', codigoQR=codigoQR, correoelectronico = miVariableCorreoElectronicoAdministrador)); 


########################### endpoints Administrador con el robot. #####################################################################################################################################################################################
@app.route ("/administradorsignup", methods = ['GET', 'POST'])
@app.route ("/administradorsignup/<tokenrestablecercontrasena>", methods = ['GET', 'POST'])
def funcionAdministradorsignup (tokenrestablecercontrasena = None):
    miVariableContrasenasNoCoinciden = False;
    miVariableUsuarioYaCreado = False;
    miFormulario = formulario.FormularioAcceder (request.form);
    if (request.method == 'POST'):
        if (tokenrestablecercontrasena != None):
            miVariableCorreoAdministrador = None;
            fechaDeCreacionDelTokenRestablecerContrasena = None;
            for clave in miDiccionarioCorreoElectroncoYtokenRestablecerContrasena:
                if (miDiccionarioCorreoElectroncoYtokenRestablecerContrasena[clave][0] == tokenrestablecercontrasena):
                    miVariableCorreoAdministrador = clave;
                    fechaDeCreacionDelTokenRestablecerContrasena = miDiccionarioCorreoElectroncoYtokenRestablecerContrasena[clave][1];
                    break;
            if (miVariableCorreoAdministrador == None) or ((datetime.now() - fechaDeCreacionDelTokenRestablecerContrasena) >= timedelta (minutes=10)):
                return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorsignup.html --- Error401 --- El token de para cambiar la contrsaeña, no identifica a nungun administrador en el sistema o ha caducado. "));  
            else:
                miAdministradores = Administradores.query.filter_by (_correoElectronico = miVariableCorreoAdministrador).first ();
                if (miAdministradores == None):
                    return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorsignup.html --- Error404  ----  El token sí aparece en el sistema, pero ese administrador no esta en la base de datos. "));  
                else:
                    if (miFormulario.contrasena.data != miFormulario.confirmarContrasena.data):
                        miVariableContrasenasNoCoinciden = True;
                    else:
                        miContrasenaHaseada = generate_password_hash (miFormulario.contrasena.data);
                        miAdministradores._contrasena = miContrasenaHaseada;
                        db.session.commit ();
                        del (miDiccionarioCorreoElectroncoYtokenRestablecerContrasena [miVariableCorreoAdministrador]);
                        return redirect (url_for ('funcionAdministradorLogin'));
        else:
            miAdministradores = Administradores.query.filter_by (_correoElectronico = miFormulario.correoElectronico.data).first ();
            if (miAdministradores):
                miVariableUsuarioYaCreado = True;
            else:
                if (miFormulario.contrasena.data != miFormulario.confirmarContrasena.data):
                    miVariableContrasenasNoCoinciden = True;
                else:
                    miContrasenaHaseada = generate_password_hash (miFormulario.contrasena.data);
                    miAdministradores = Administradores (_correoElectronico=miFormulario.correoElectronico.data, _contrasena=miContrasenaHaseada);
                    db.session.add (miAdministradores);
                    db.session.commit ();
                    return redirect (url_for ('funcionAdministradorLogin'));
    return (render_template ("administradorsignup.html", miFormularioParametro=miFormulario, miParametroContrasenasNoCoinciden=miVariableContrasenasNoCoinciden, miParametroUsuarioYaCreado = miVariableUsuarioYaCreado, miPrametroTokenRestablecerContrasena = tokenrestablecercontrasena));


@app.route ("/administradorlogin", methods = ['GET', 'POST'])
def funcionAdministradorLogin ():
    miFormulario = formulario.FormularioAcceder (request.form);
    miVariableUsuarioIncorrecto = False;
    miVariableContrasenaIncorrecta = False;
    miVariableRecuperarCorreo = False;
    if (request.method == 'POST'):
        miAdministradores = Administradores.query.filter_by (_correoElectronico=miFormulario.correoElectronico.data).first ();
        if (miAdministradores != None):
            if ("nameformularioacceder" in request.form):
                if (miAdministradores.validarContrasena (miFormulario.contrasena.data)):
                    session['correoElectronico'] = miAdministradores._correoElectronico;
                    return redirect (url_for ('funcionAdministradorHome'));
                else:
                    # en este caso la contraseña pasada, no coincide con el HASH, por lo tanto contraseña incorrecta.
                    miVariableContrasenaIncorrecta = True;
            else:
                if ("nameformulariorecuperarcontrasena" in request.form):
                    try:
                        miDiccionarioCorreoElectroncoYtokenRestablecerContrasena[miAdministradores._correoElectronico] = [os.urandom(12).hex(), datetime.now()]; 
                        miMensaje = Message (subject="Demostraciones robóticas, solicitud de cambio de contraseña.", body="Buenas se ha solicitado un cambio de contraseña en el página web de demostracione robóticas, sí desea cambiarla acceda aquí: http://localhost:5000/administradorsignup/" +miDiccionarioCorreoElectroncoYtokenRestablecerContrasena[miAdministradores._correoElectronico][0],
                                          sender= app.config['MAIL_USERNAME'], recipients=[miAdministradores._correoElectronico]);
                        mail.send (miMensaje);
                        miVariableRecuperarCorreo = True;
                    except Exception as e:
                        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorlogin.html ---Error500  --- error al enviar el correo electrónico"));  
                else:
                    return redirect (url_for ('funcionErrorClienteServidor', mensajeerror = "administradorlogin.html --- Error500 --- formulario inválido"));
        else:
            #en este caso ni si quiera se ha encontrado a ese correo de administrador en la BBDD. 
            miVariableUsuarioIncorrecto = True;
            
    return (render_template("administradorlogin.html", miFormularioParametro = miFormulario, miParametroUsuarioIncorrecto = miVariableUsuarioIncorrecto, miParametroContrasenaIncorrecta = miVariableContrasenaIncorrecta, miParametroRecuperarCorreo=miVariableRecuperarCorreo));

@app.route ("/administradorcerrarsesion")
def funcionAdministradorCerrarSesion ():
    session.pop ('correoElectronico');
    return redirect (url_for ('funcionAdministradorLogin'));


@app.route('/administradorhome')   
def funcionAdministradorHome():
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();

    miVariableCantidadDeEventosDelAdminstrador = len (miAdministradores.funcion_conseguirTodosLosEventosDeEseAdministrador());
    miVariableCantidadDeAsistentesDelAdministrador = len(miAdministradores.funcion_conseguirTodosLosAsistentesDelAdministrador());
    miVariableCantidadRobotsQueUsoEnEventosAdministrador = len (miAdministradores.funcion_conseguirRobotsQueUsoEnEventosAdministrador ());
    miVariableCantidadRobotsQueUsoEnEventosAdministradorSinServicioActualmente = len (miAdministradores.funcion_conseguirListaDisponibleRobotEventosDelAdministradorSinServicioActualmente());

    miVariableCantidadDeEventosEnElSistema = len (miAdministradores.funcion_conseguirTodosLosEventos());
    miVariableCantidadAsistentensEnElSistema = len (miAdministradores.funcion_conseguirTodosLosAsistentesDelSistema ());
    miVariableCantidadRobotsEnElSistema = len (miAdministradores.funcion_conseguirTodosLosRobots ());
    miVariableCantidadRobotsSinServicioEnElSistema = len (miAdministradores.funcion_conseguirListaEventosQueTienenAlmenosUnRobotEsperandoPorAsistentes ());    

    return (render_template ("administradorhome.html", parametroCantidadDeEventosDelAdministrador=miVariableCantidadDeEventosDelAdminstrador, parametroCantidadDeAsistentesDelAdministrador=miVariableCantidadDeAsistentesDelAdministrador, parametroCantidadRobotsDelAdminstrador=miVariableCantidadRobotsQueUsoEnEventosAdministrador,
    parametroRobotsQueUsoEnEventosAdministradorSinServicioActualmente=miVariableCantidadRobotsQueUsoEnEventosAdministradorSinServicioActualmente, parametroCantidadDeEventosEnElSistema=miVariableCantidadDeEventosEnElSistema, parametroCantidadAsistentesEnElSistema=miVariableCantidadAsistentensEnElSistema, 
    parametroCantidadDeRobotsEnElSistema=miVariableCantidadRobotsEnElSistema, parametroCantidadRobotsSinServicioEnElSistema = miVariableCantidadRobotsSinServicioEnElSistema, parametroCorreoElectronico = miAdministradores._correoElectronico));
   


@app.route ('/administradorpanelrobot/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
@app.route ('/administradorpanelrobot')
def funcionAdministradorPanelRobot (nombreDelEvento = None, fechaDeCreacionDelEvento = None, lugarDondeSeCelebra = None):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioBuscarRobot (request.form);

    miListaDeEventos = miAdministradores.funcion_conseguirTodosLosEventos ();
    miMostrarRobotsNingunEvento = False;
    miListaRobots = [];

    if ((nombreDelEvento == None) and (fechaDeCreacionDelEvento == None) and (lugarDondeSeCelebra == None)):
        miListaRobots = miAdministradores.funcion_conseguirRobotsQueNoEstanEnNingunEvento();
        miMostrarRobotsNingunEvento = True;
    else:
        if ((nombreDelEvento == "todosLosRobots") and (fechaDeCreacionDelEvento == "todosLosRobots") and (lugarDondeSeCelebra=="todosLosRobots")):
            if (request.method == 'POST'):
                if (miFormulario.campoBuscadorRobotSelect.data == "MAC"):
                    miListaRobots = miAdministradores.funcion_conseguirTodosLosRobotsPorMacAddressDelRobot (miFormulario.campoBuscadorRobotString.data);  
                else:
                    miListaRobots = miAdministradores.funcion_conseguirTodosLosRobotsPorNombreDelRobot (miFormulario.campoBuscadorRobotString.data);
            else:
                miListaRobots = miAdministradores.funcion_conseguirTodosLosRobots();
        else:
            miListaDisponibleRobot = miAdministradores.funcion_conseguirDisponibleRobotPorEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
            for miDisponibleRobotObjeto in miListaDisponibleRobot:
                miRobot = miAdministradores.funcion_conseguirRobotPorIdRobot (miDisponibleRobotObjeto.robots_idRobot);
                if (miRobot not in miListaRobots): # aqui sólo añado los robots que no se repiten, por eso compruebo primero si esta.
                    miListaRobots.append (miRobot);
    miFormulario.campoBuscadorRobotSelect.choices = ["MAC", "Nombre del robot"];
    return render_template ("administradorpanelrobot.html", miListaRobotsParametro=miListaRobots, miListaDeEventosParametro=miListaDeEventos, miParametroMostrarRobotsNingunEvento=miMostrarRobotsNingunEvento, parametroNombreDelEvento = nombreDelEvento, miFormularioParametro=miFormulario);


@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>')
def funcionAdministradorPanelRobotBorrar (idRobot, nombreDelEvento=None, fechaDeCreacionDelEvento=None, lugarDondeSeCelebra=None):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miRobots = miAdministradores.funcion_conseguirRobotPorIdRobot (idRobot);
    if (miRobots == None):
        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="adminstradorpanelrobotborrar.html  --- Error404 --- No se puede modificar el robot, ya que el robot que has puesto no existe en la BBDD ")); 
    else: 
        if (miAdministradores.funcion_verSiPuedoBorrarRobot (idRobot) == False):
            return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorpaneleventoborrar.html --- Error403--- ese administrador, no puede eliminar ese robot."));  

    miAdministradores.funcion_borrarRobot (idRobot);

    if ((nombreDelEvento == None) and (fechaDeCreacionDelEvento == None) and (lugarDondeSeCelebra == None)):
        return redirect (url_for ('funcionAdministradorPanelRobot'));
    else:
        return redirect (url_for ('funcionAdministradorModificarRobotsEvento', nombreDelEvento = nombreDelEvento, fechaDeCreacionDelEvento = fechaDeCreacionDelEvento, lugarDondeSeCelebra = lugarDondeSeCelebra));

@app.route ('/administradorcrearrobot', methods = ['GET', 'POST'])
def funcionAdministradorCrearRobot ():
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCreaRobot (request.form);
    # ya que administradorcrearrobot.html lo utilizo en crear robot, modificar roboot y en modificar robot cuando estoy dentro del evento, el nombreDelEvento, fechaDeCreacionDelEvento y lugarDondeSeCelebra se establecen en Null,
    # para saber que desde este endpint administradorcrearrobot, después de que se cree, no se tiene que volver a ningun evvento. 

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
            # en el caso de que la foto pesa más de 5MB, devuelvo un error. 
            if ((len(binarioDeFoto)/1024) > 10240):
                return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorcrearrobot.html --- Error400 ---el archivo dede de pesar como máximo 10MB. "));  
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
                    return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorcrearrobot.html --- Error400 ---la extesión del archivo no es valida, las extensiones permitidas son .jpg .jpeg y .png"));  
            miFotoDelFormulario = Image.open (BytesIO (binarioDeFoto));
            try:
                miFotoDelFormulario = ImageOps.exif_transpose(miFotoDelFormulario);
            except Exception as e:
                return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorcrearrobot.html  --- Error500 --- Esa foto no se puede procesar, hay error en los metadatos EXIF. ")); 
            miFotoDelFormulario.thumbnail ((300,300), Image.Resampling.LANCZOS);
            miByte_io = BytesIO();
            if (miVerdadEsJPG) or (miVerdadEsJPEG):
                miFotoDelFormulario.save (miByte_io, 'jpeg');
            else:
                miFotoDelFormulario.save (miByte_io, 'png');
            binarioDeFoto = miByte_io.getvalue();  
            miAdministradores.funcion_crearRobot (miFormulario.macAddressDelRobot.data, miFormulario.nombreDelRobot.data, binarioDeFoto, miFormulario.descripcionDelRobot.data);
        return redirect(url_for('funcionAdministradorPanelRobot'));

    return render_template ('administradorcrearrobot.html', miFormularioParametro = miFormulario, miParametroAccionHtml = "crear", miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento= fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra= lugarDondeSeCelebra, parametroMACaddressDelRobot=None);



# en esta parte dejo la posibilidad de que este endpoint no reciba el evento, ya que puedde ser que se modifique un robot desde el panel robot, el cual muestra todos los robots que no estan en ningun evento, y recordar que en esta parte cualquier administrador
#puede modificar un robot, por lo tanto despues de modificarlo la pantalla de muestra no tiene porque ser la de gestion de robots en evento, si no que puede ser que se quede en la misma pudiendo modificar mas robots. 
@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>', methods = ['GET', 'POST'])
@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobotModificar (idRobot, nombreDelEvento = None, fechaDeCreacionDelEvento = None, lugarDondeSeCelebra = None):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCreaRobot (request.form);

    miRobots = miAdministradores.funcion_conseguirRobotPorIdRobot (idRobot);
    if (miRobots == None):
        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="adminstradorpanelrobotmodificar.html --- Error404 --- No se puede modificar el robot, ya que el robot que has puesto no existe en la BBDD ")); 
    if (request.method == 'POST'):
        if (miFormulario.validate()):
            fotoRecibidaDelFormulario = request.files['fotoDelRobot'];
            binarioDeFoto = fotoRecibidaDelFormulario.read();
            if (len(binarioDeFoto) == 0):
                binarioDeFoto = None;
            else:
                if ((len(binarioDeFoto)/1024) > 10240):
                    return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="adminstradorpanelrobotmodificar.html --- Error400 ---el archivo dede de pesar como máximo 10MB. "));  
                else:
                    miExpresionRegularParaJPG = r".+\.jpg$";
                    miExpresionRegularParaJPEG = r".+\.jpeg$";
                    miExpresionRegularParaPNG = r".+\.png$";
                    miVerdadEsJPG = bool(re.match (miExpresionRegularParaJPG, fotoRecibidaDelFormulario.filename));
                    miVerdadEsJPEG = bool(re.match (miExpresionRegularParaJPEG, fotoRecibidaDelFormulario.filename));
                    miVerdadEsPNG = bool(re.match (miExpresionRegularParaPNG, fotoRecibidaDelFormulario.filename));
                    if (miVerdadEsJPG == False) and (miVerdadEsJPEG == False) and (miVerdadEsPNG == False):
                        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="adminstradorpanelrobotmodificar.html --- Error400 ---la extesión del archivo no es valida, las extensiones permitidas son .jpg .jpeg y .png")); 
                miFotoDelFormulario = Image.open (BytesIO (binarioDeFoto));
                try:
                    miFotoDelFormulario = ImageOps.exif_transpose(miFotoDelFormulario);
                except Exception as e:
                    return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="adminstradorpanelrobotmodificar.html  --- Error500 --- Esa foto no se puede procesar, hay error en los metadatos EXIF. ")); 
                miFotoDelFormulario.thumbnail ((300,300), Image.Resampling.LANCZOS);
                miByte_io = BytesIO();  
                if (miVerdadEsJPG) or (miVerdadEsJPEG):
                    miFotoDelFormulario.save (miByte_io, 'jpeg');
                else:
                    miFotoDelFormulario.save (miByte_io, 'png');                
                binarioDeFoto = miByte_io.getvalue();
            miAdministradores.funcion_modificarRobot (idRobot, miFormulario.macAddressDelRobot.data, miFormulario.nombreDelRobot.data, binarioDeFoto, miFormulario.descripcionDelRobot.data);

            if ((nombreDelEvento == None) and (fechaDeCreacionDelEvento == None) and (lugarDondeSeCelebra == None)):
                return redirect(url_for('funcionAdministradorPanelRobot')); 
            else:   
                return redirect (url_for ('funcionAdministradorModificarRobotsEvento', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra));
        else:
            # en el caso de que no se valide el formulario, lo que hago es que devuelvo el formulario con los datos que se acaban de rellenar por el request.form y en este ya está almacenado el error. 
            return render_template ("administradorcrearrobot.html", miFormularioParametro=miFormulario, miParametroAccionHtml="modificar", miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento= fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra= lugarDondeSeCelebra,
                                    parametroMACaddressDelRobot=miRobots._macAddressDelRobot);
    else:
        #en el caso de que un administrador vea un robot, sabiendo que esta en la tabla de disponible, pero que ademas ese robot lo estan utilizando actualmente, entonces no se le va a mostrar la opcion de modificar, pero lo que pasa es que si el pone en la URL
        # a este robot, entonecs sí que lo puede modificar, por lo tanto hago este if que vuelve a comprobar si ese administrador lo puede o no modificar, en el caso de que no pueda, le mando un error. 
        if (miAdministradores.funcion_verSiPuedoModificarRobot (idRobot) == False):
            return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorpaneleventoborrar.html --- error403 --- ese administrador, no puede modificcar ese robot, ya que otro adminsitrador lo esta usando actualmente. ")); 
        else:
            miFormulario.macAddressDelRobot.data = miRobots._macAddressDelRobot; 
            miFormulario.nombreDelRobot.data = miRobots._nombreDelRobot; 
            miFormulario.descripcionDelRobot.data = miRobots._descripcionDelRobot; 

            return render_template ("administradorcrearrobot.html", miFormularioParametro=miFormulario, miParametroAccionHtml="modificar", miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento= fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra= lugarDondeSeCelebra, 
                                    parametroMACaddressDelRobot=miRobots._macAddressDelRobot);

########################### endpoints Administrador con los eventos #####################################################################################################################################################################################

@app.route ('/administradorpanelevento/<int:miVerdadErrorDeEventoInexistente>')
@app.route ('/administradorpanelevento')
def funcionAdministradorPanelEvento (miVerdadErrorDeEventoInexistente = 0):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miListaEventos = miAdministradores.funcion_conseguirTodosLosEventosDeEseAdministrador ();
    return render_template ("administradorpanelevento.html", parametroURL = miVariableGlobalURL, miListaEventosParametro=miListaEventos, miParametroVerdadErrorDeEventoInexistente=miVerdadErrorDeEventoInexistente, parametroCorreoElectronico = miAdministradores._correoElectronico);


@app.route ('/administradorpaneleventoborrar/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
def funcionAdministradorPanelEventoBorrar (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miEventos = miAdministradores.funcion_conseguirEventoPorClavePrimaria (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
    if (miEventos == None):
        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorpaneleventoborrar.html ---  error404--- No se puede borrar el evento, ya que no existe en la BBDD.")); 
    
    if (miAdministradores.funcion_verSiEseEventoEsDeEseAdministrador  (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra)):
        miAdministradores.funcion_borrarEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
        return redirect (url_for ('funcionAdministradorPanelEvento'));
    else:
        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradorpaneleventoborrar.html --- error404  --- para ese adminstrador, ese evento no existe")); 


@app.route ('/administradorcrearevento', methods = ['GET', 'POST'])
def funcionAdministradorCrearEvento ():
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miFormulario = formulario.FormularioCrearEvento (request.form);

    if (request.method == 'POST') and (miFormulario.validate ()): 
        miAdministradores.funcion_crearEvento (miFormulario.nombreDelEvento.data, miFormulario.lugarDondeSeCelebra.data, miFormulario.codigoQR.data);
        return redirect (url_for ('funcionAdministradorPanelEvento'));

    return render_template ("administradorcrearevento.html", parametroURL = miVariableGlobalURL, miFormularioParametro = miFormulario, miParametroAccionHtml = "crear");

@app.route ('/administradormodificardatosevento/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
def funcionAdministradorModificarDatosEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miEventos = miAdministradores.funcion_conseguirEventoPorClavePrimaria (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
    if (miEventos == None):
        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradormodificardatosevento.html --- error404 ---  No se puede modificar el evento ya que ese evento no existe")); 

    miFormulario = formulario.FormularioCrearEvento (request.form);

    if (request.method == 'POST'):
        if (miFormulario.validate()):
            miVariableMensajeDeError = None;
            miVariableMensajeDeError = miAdministradores.funcion_modificarDatosDelEvento (nombreDelEvento, miFormulario.fechaDeCreacionDelEvento.data, lugarDondeSeCelebra, miFormulario.nombreDelEvento.data,  miFormulario.lugarDondeSeCelebra.data, miFormulario.codigoQR.data);
            if (miVariableMensajeDeError != None):
                return redirect (url_for ('funcionErrorClienteServidor', mensajeerror=miVariableMensajeDeError)); 
            return redirect(url_for('funcionAdministradorPanelEvento'));
        else:
            return render_template ("administradorcrearevento.html", parametroURL = miVariableGlobalURL, miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar");
    else:
        if (miAdministradores.funcion_verSiEseEventoEsDeEseAdministrador  (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra)):
            miEventos = miAdministradores.funcion_conseguirEventoPorClavePrimaria (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra)
            miFormulario.nombreDelEvento.data = miEventos._nombreDelEvento;
            miFormulario.fechaDeCreacionDelEvento.data = miEventos._fechaDeCreacionDelEvento;
            miFormulario.lugarDondeSeCelebra.data = miEventos._lugarDondeSeCelebra;
            miFormulario.codigoQR.data = miEventos._codigoQR;
            return render_template ("administradorcrearevento.html", parametroURL = miVariableGlobalURL, miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar");
        else:
            return redirect(url_for('funcionAdministradorPanelEvento', miVerdadErrorDeEventoInexistente=1));

@app.route ('/administradormodificarrobotsevento/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>', methods = ['GET', 'POST'])
def funcionAdministradorModificarRobotsEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();

    if (request.method == 'POST'):
        if ('nameformulariomodificar' in request.form):
            miVariableMensajeDeError = None;
            miVariableMensajeDeError = miAdministradores.funcion_modificarRobotDelEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, request.form.get('robots_idRobot'), request.form.get('fechaComienzoEnEventoAntigua'), request.form.get('fechaFinEnEventoAntigua'), 
                                                               request.form.get('fechaComienzoEnEvento'), request.form.get('fechaFinEnEvento'), request.form.get ('disponible'));
            if (miVariableMensajeDeError != None):
                return redirect (url_for ('funcionErrorClienteServidor', mensajeerror=miVariableMensajeDeError)); 
        else:
            if ("nameformulariosumarrobot" in request.form):
                miDisponibleRecibido = request.form.get ('disponible');
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
                miAdministradores.funcion_sumarRobotAlEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, miIdRobotRecibido, miFechaComienzoEnEventoRecibido, miFechaFinEnEventoRecibido, miDisponibleRecibido);
            else:
                if ("nameformularioeliminar" in request.form):
                    miVariableMensajeDeError = None;
                    miVariableMensajeDeError = miAdministradores.funcion_eliminarRobotDelEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra, request.form.get('robots_idRobot'), request.form.get('fechaComienzoEnEventoAntigua'), request.form.get('fechaFinEnEventoAntigua'));
                    if (miVariableMensajeDeError != None):
                        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror=miVariableMensajeDeError)); 
                else:
                    return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="administradormodificarrobotsevento.htmml --- Error500 --- formulario invalido.")); 
    
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
            miVariablePuedoeliminar = miAdministradores.funcion_verSiPuedoBorrarRobot (clave._idRobot);
            miDisponibleRobotActualmente = miAdministradores.funcion_conseguirDisponibleRobotPorIdRobotYporEstarContempladaLaFechaDelSistema (clave._idRobot)
            miVariableQueBotonEnServicioEs = not(miDisponibleRobotActualmente.disponible);
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
            miVariablePuedoeliminar = miAdministradores.funcion_verSiPuedoBorrarRobot (clave._idRobot);
            miVariablePuedoModificar = miAdministradores.funcion_verSiPuedoModificarRobot (clave._idRobot);
            miDiccionarioRobotsActualmenteNoEstanEnEvento[clave] = {"subclaveListas":miDiccionarioRobotsActualmenteNoEstanEnEvento[clave], "subclavePuedoModificar": miVariablePuedoModificar, "subclavePuedoeliminar": miVariablePuedoeliminar};

        # este for me vale para rellenar los formularios de los robots que no estan en ese evento. tabla 3. (la de abajo del todo).
        miListaDeSumarRobot = [];
        for miRobotObjeto in miAdministradores.funcion_conseguirTodosLosRobotsQueNoSonDeEseEvento (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra): 
            miListaDeSumarRobot.append ([miRobotObjeto._idRobot, miRobotObjeto._macAddressDelRobot]);
        miVariablePorcentajeAsistentesQueSiHanControladoUnRobot = miAdministradores.funcion_conseguirPorcentajeAsistentesQueSiHanControladoUnRobot (nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra);
        miVariableCantidadDeAsistentesVinculadosEnElEvento = len (miAdministradores.funcion_conseguirTodosLosAsistentesVinculadosAlEvento(nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra));
        return render_template ("administradormodificarrobotsevento.html", miDiccionarioRobotsActualmenteEstanEnEvetoParametro=miDiccionarioRobotsActualmenteEstanEnEvento, miDiccionarioRobotsActualmenteNoEstanEnEvetoParametro=miDiccionarioRobotsActualmenteNoEstanEnEvento,
                                 miListaDeSumarRobotParametro=miListaDeSumarRobot, miParametroNombreDelEvento=nombreDelEvento, miParametroFechaDeCreacionDelEvento=fechaDeCreacionDelEvento, miParametroLugarDondeSeCelebra=lugarDondeSeCelebra, 
                                 miParametroPorcentajeAsistentesQueSiHanControladoUnRobot = miVariablePorcentajeAsistentesQueSiHanControladoUnRobot, miParametroCantidadDeAsistentesVinculadosEnElEvento = miVariableCantidadDeAsistentesVinculadosEnElEvento,
                                 miParametroFechaActualDelSistema = datetime.now ());
    else:
        return redirect(url_for('funcionAdministradorPanelEvento', miVerdadErrorDeEventoInexistente=1))


@app.route ('/adminstradorpanelrobotponerservicio/<int:idRobot>/<int:robotEnServicio>/<nombreDelEvento>/<fechaDeCreacionDelEvento>/<lugarDondeSeCelebra>')
def funcionAdministradorPanelRobotPonerServicio (idRobot, robotEnServicio, nombreDelEvento, fechaDeCreacionDelEvento, lugarDondeSeCelebra): 
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first(); 
    # este if lo pongo, ya que en el caso de que otro administrador conozca el idRoot y el evento en el que etá, puede modificar el servicio del robot, por lo tanto para evitar eseo, copruebo que es el dueño del robot
    #el que esta modificando el servicio del robot. 
    if (miAdministradores.funcion_verSiPuedoModificarRobot (idRobot) == False):
        return redirect (url_for ('funcionErrorClienteServidor', mensajeerror="adminstradorpanelrobotponerservicio  --- Error403---  ese administrador no puede modificar el servicio de ese robot, ya que actualmente la hora de trabajo de este robot no se corresponde con ningun evento de este administrador. ")); 
    miAdministradores.funcion_activarOdesactivarRobot (idRobot, robotEnServicio);
    return redirect (url_for ('funcionAdministradorModificarRobotsEvento', nombreDelEvento=nombreDelEvento, fechaDeCreacionDelEvento=fechaDeCreacionDelEvento, lugarDondeSeCelebra=lugarDondeSeCelebra));




########################### endpoints Administrador con las cuentas #####################################################################################################################################################################################
@app.route ('/administradorpaneladministradorgestioncuentas')
def funcionAdministradorGestioncuentas ():
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first();
    miListaAdministradores = miAdministradores.funcion_conseguirTodasLasCuentasMenosLaInstanciada ();
    miDiccionarioAdministradores = {};
    miListaDeEventos = [];
    for i in miListaAdministradores:
        miListaDeEventos = miAdministradores.funcion_conseguirTodosLosEventosPorCorreoElectronico (i._correoElectronico);
        miDiccionarioAdministradores[i._correoElectronico] = miListaDeEventos;
    return render_template ("administradorpanelgestioncuentas.html", miParametroDiccionarioAdministradores = miDiccionarioAdministradores);

@app.route ('/administradorborrarcuentaadministrador/<correoelectronico>')
def funcionAdministradorBorrarCuentaAdministrador (correoelectronico):
    miAdministradores = Administradores.query.filter_by (_correoElectronico=session['correoElectronico']).first ();
    miAdministradores.funcion_borrarCuentaAdministrador (correoelectronico);
    
    return redirect (url_for ('funcionAdministradorGestioncuentas'));

######## Configuración de Flask.  ##################################################################################################################################################################################################################

# este if es algo clásico de python, y es que en el caso de que se importe este main, no se van a ejecutar las lineas que están arriba en el momento de hacer ei import, gracias 
# a este if. De esta manera tengo más control sobre la ejecución y es que a esas funcones de arriba las puedo llamar en cualquier momento.  
if __name__ == '__main__':
    # a la hora de poner los formularios, necesito que tengan un token para verrificar que el me envia los datos de nuevo al servidor, que sea el cliente correcto.  
    csrf.init_app(app);


    # esto lo que hace es aplicar la configuracion de la base datos hecha en el archivo condig.py 
    db.init_app (app);

    # esto es para explicar bajo que contexto,  vamos a crear la DDBB, es decir que vamos a aplicar la configuración que tenemos en el app, el cual hemos configurado en el 
    # archivo config.py con la clase: DevelopmentConfig. De manera que este with es necesario para que se tenga en cuenta la configuración. 
    with app.app_context ():
        db.create_all (); #esto se encarga de crear las tablas que no esten creadas en el modelo. 
        
    app.run(debug=app.config['DEBUG'], port=app.config['PORT']);



