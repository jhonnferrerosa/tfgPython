

# el request,  me vale para recibir parámetros por a URL. 
# el redirect me vale para redirigir a los usuarios a otra pagina de mi aplicacion. 
# el url_for genera una url para una de las funciones que tengo en este main.py. 
from flask import Flask, request, render_template, redirect, url_for, session

from models import db
from config import DevelopmentConfig  #Desde mi archivo config.py importo esta clase. 

from models import Administradores, Robots, Eventos, Asistentes, Vincula, DisponibleRobot, Controla

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
    miAdmin1 = Administradores (correoElectronico="jhon@gmail.com", contrasena="james");
    db.session.add (miAdmin1);
    db.session.commit ();

    miEvento1 = Eventos (nombreDelEvento="aula1", fechaDeCreacionDelEvento='2024-10-01', lugarDondeSeCelebra="ifema1", codigoQR="miQR1", administradores_correoElectronico="jhon@gmail.com");
    miEvento2 = Eventos (nombreDelEvento="puertas abiertas1", fechaDeCreacionDelEvento='2024-10-01', lugarDondeSeCelebra="alcala", codigoQR="miQR2", administradores_correoElectronico="jhon@gmail.com");
    miEvento3 = Eventos (nombreDelEvento="simo1", fechaDeCreacionDelEvento='2024-10-01', lugarDondeSeCelebra="torrejon", codigoQR="miQR3", administradores_correoElectronico="jhon@gmail.com");
    db.session.add (miEvento1);
    db.session.add (miEvento2);
    db.session.add (miEvento3);
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
    db.session.add (miRobot1);
    db.session.add (miRobot2);
    db.session.add (miRobot3);
    db.session.add (miRobot4);
    db.session.add (miRobot5);
    db.session.commit ();

    miVincula1 = Vincula (asistentes_identificadorUnicoAsistente="IUA1", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula2 = Vincula (asistentes_identificadorUnicoAsistente="IUA2", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula3 = Vincula (asistentes_identificadorUnicoAsistente="IUA3", eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    miVincula4 = Vincula (asistentes_identificadorUnicoAsistente="IUA4", eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", fechaAcceso="2024-11-01", fechaSalida="2024-11-30");
    db.session.add (miVincula1);
    db.session.add (miVincula2);
    db.session.add (miVincula3);
    db.session.add (miVincula4);
    db.session.commit ();

    miDisponibleRobot1 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot2 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-12-01", fechaFinEnEvento="2024-12-30");
    miDisponibleRobot3 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=102 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot4 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=104 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    miDisponibleRobot5 = DisponibleRobot (eventos_nombreDelEvento="puertas abiertas1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="alcala", robots_idRobot=105 , fechaComienzoEnEvento="2024-10-01", fechaFinEnEvento="2024-10-30");
    db.session.add (miDisponibleRobot1);
    db.session.add (miDisponibleRobot2);
    db.session.add (miDisponibleRobot3);
    db.session.add (miDisponibleRobot4);
    db.session.add (miDisponibleRobot5);
    db.session.commit ();

    miControla1 = Controla (asistentes_identificadorUnicoAsistente="IUA1", robots_idRobot=101, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now() + timedelta(minutes=5));
    miControla2 = Controla (asistentes_identificadorUnicoAsistente="IUA2", robots_idRobot=102, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now() + timedelta(minutes=5));
    db.session.add (miControla1);
    db.session.add (miControla2);
    db.session.commit ();

    return "<p> este es el index2 </p>"

@app.route ("/index3")
def index3 ():
    miEvento = Eventos.query.filter_by (_Eventos__nombreDelEvento="aula1").first ();
    miEvento.fechaDeCreacionDelEvento='2024-11-05';
    db.session.commit ();
    return "<p> este es el index 3 </p>";


@app.route ("/index4")
def index4 ():
    miEvento = Eventos.query.filter_by (_Eventos__nombreDelEvento="aula1").first ();
    db.session.delete (miEvento);
    db.session.commit ();
    return "<p> este es el index4. </p>";

@app.route ("/index5")
def index5 ():
    return "<p> este es el index5.  </p>";

@app.route ("/index6")
def index6 ():
    return "<p>  este es el index 6";

@app.route ("/index7")
def index7 ():

    return "<p>  este es el index 7";

@app.route ("/index8")
def index8 ():
    return "<p> este es el index8.  </p>";

@app.route ("/index9")
def index9 ():
    return "<p> este es el index9 </p>";

######## endpoints Asistente. ############################################################################################################################################################################################################




    
########################### endpoints Administrador. ################################################################################################################################################################################################# 


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



