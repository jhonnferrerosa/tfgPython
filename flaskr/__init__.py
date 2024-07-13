from flask import Flask
from flask import render_template
from flask_wtf import CSRFProtect
from models import db
from config import DevelopmentConfig
import formulario
from flask import request

from flask import url_for
from flask import redirect 

from flask import session

from models import Asistente
from models import Evento
from models import LugarDelEvento
from models import Robot

from datetime import datetime 

import os

import threading  # esta libreria (1/3) es para los hilos. 
from flask import copy_current_request_context  # esta libreria (2/3) es para los hilos. 
import time  # esta libreria (3/3) es para los hilos. 

# https://www.demosroboticas.com primera pagina para los asistentes. 
# https://www.demosroboticas.com/robotlisto
#  https://www.demosroboticas.com/esperando 


#  https://www.demosroboticas.com/administradorhome
#  https://www.demosroboticas.com/administradorpanelrobot
#  https://www.demosroboticas.com/administradordatosrobot

# https://www.demosroboticas.com/administradorcuentas
# https://www.demosroboticas.com/administradorpanelevento
#  https://www.demosroboticas.com/administradoreditardatosevento

app = Flask(__name__);  
app.config.from_object (DevelopmentConfig);

csrf = CSRFProtect ();


miDiccionarioGloalTokensEnteros = None;

def funcionEliminaAsistenteDeLaBaseDeDatos (tokenDeSesion):
	time.sleep (10);
	print ("funcionEliminaAsistenteDeLaBaseDeDatos()--- en ese token, esta es la cantidad de intentos: ", miDiccionarioGloalTokensEnteros[tokenDeSesion]);
	if (miDiccionarioGloalTokensEnteros[tokenDeSesion] == 0):  # en este caso si que puedo borrar de la BBDD. 
		miAsistente = Asistente.query.filter_by (tokenDeSesion=tokenDeSesion).first();
		if (miAsistente != None): # esto lo hago para ahorrarme el problema de que si por algun casual se intenta borrar varias veces, que la web no de error de integridad. 
			db.session.delete(miAsistente);
			db.session.commit();	
	else:
		print ("funcionEliminaAsistenteDeLaBaseDeDatos()---  No se borra de la BBDD");
		print ("funcionEliminaAsistenteDeLaBaseDeDatos()---  ", miDiccionarioGloalTokensEnteros[tokenDeSesion]);
		miDiccionarioGloalTokensEnteros[tokenDeSesion] -= 1;

@app.before_request 
def miFuncionAntesDeLaPeticion (): 
	print  ("miFuncionAntesDeLaPeticion() --- este es el endpoint: ", request.endpoint); 

	if (request.endpoint == "funcionCierraNavegador"):
		print  ("miFuncionAntesDeLaPeticion() --- se va a eliminar en la BBDD: ", session.get('token'));
		if (session.get('token') != None):  # esto puede venir bien porque este endpoint se ejecuta antes tambien para los adminstradores. 
			miToken = session.get('token');

			@copy_current_request_context
			def sendHiloFuncionEliminaAsistenteDeLaBaseDeDatos (miToken):
				funcionEliminaAsistenteDeLaBaseDeDatos (miToken);

			hiloFuncionEliminaAsistenteDeLaBaseDeDatos = threading.Thread (name="hiloFuncionEliminaAsistenteDeLaBaseDeDatos", target=sendHiloFuncionEliminaAsistenteDeLaBaseDeDatos, args=(miToken,));
			hiloFuncionEliminaAsistenteDeLaBaseDeDatos.start();


@app.route('/')   
def funcionIndex():
	#  TO DO: seria buena idea poner que en el momento en el que se ingrese un asistente nuevo, que se compruebe que todos llevan activos desdde hace menos de 12 horas. 
	global miDiccionarioGloalTokensEnteros; 
	if (('token' in session) == False):
		session['token'] = os.urandom(24).hex();  # Genera un token de sesión único
		miDiccionarioGloalTokensEnteros = {session.get('token'): 0}  # establezco que ese token tien cero intentos de poder ser borrado por la funcionCierraNavegador en @app.before_request
		miAsistente = Asistente (tokenDeSesion=session.get('token'), apodo="elChavo", evento_idEvento=5, fechaDeAccesoAlSistema=datetime.now());
		db.session.add (miAsistente);
		db.session.commit();
		print ("funcionIndex()--- se ha crado el token.");
	else:
		print ("funcionIndex()--- ya existia una sesion: ", session.get('token'));
		# este es para el caso en el que ya se haya cerrado la sesion borrando en la base de datos, pero que se vuelva a 
		# abrir con el navegador la pagina web y le de el mismo token que el navegador recordaba antes, de manera que si 
		# no esta en la BBDD, lo que va a hacer es insertarlo otra vez. 
		if (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None):
			miDiccionarioGloalTokensEnteros = {session.get('token'): 0}  # establezco que ese token tien cero intentos de poder ser borrado por la funcionCierraNavegador en @app.before_request
			miAsistente = Asistente (tokenDeSesion=session.get('token'), apodo="elChavo", evento_idEvento=5, fechaDeAccesoAlSistema=datetime.now());
			db.session.add (miAsistente);
			db.session.commit();
			print ("funcionIndex()--- ya existia una sesion y lo he vuelto a meter en la BBDD");
		else:
			print ("funcionIndex()---", miDiccionarioGloalTokensEnteros[session.get('token')] );
			print ("funcionIndex()--- este es el tamaño del diccionario: ", len (miDiccionarioGloalTokensEnteros));
			miDiccionarioGloalTokensEnteros[session.get('token')] += 1;
			
	return (render_template("index.html"));

@app.route ('/ponerseAlaColaDeControlarUnRobot')
def functionPonerseAlaColaDeControlarUnRobot ():
	miRobot = Robot.query.filter(Robot.robotEnServicio==True, Robot.asistente_tokenDeSesion==None).first();

	if (miRobot == None): #ene se momento no hay robots disponibles. 
		print ("functionPonerseAlaColaDeControlarUnRobot()---  No hay robots. ");

	else: 	
		print ("functionPonerseAlaColaDeControlarUnRobot()--- ", miRobot.idRobot);
	return (render_template("index.html"));



@app.route('/robotlisto')
def functionRobotListo ():
	return (render_template("robotlisto.html"));

@app.route ('/esperando')
def funcionEsperando ():
	return render_template ("esperando.html");

# este endpoint no se ejecuta nunca, lo unico que neccesito que exista para que por lo menos 
# se ejecuta el codigo del @app.before_request para que de esta manera se borre la sesion 
# de la base de datos. 
@app.route ("/cierranavegador/", methods = ['POST'])
def funcionCierraNavegador ():
	return None;

@app.route('/administradorlogin', methods = ['GET', 'POST'])   
def funcionAdministradorLogin():
    print ("funcionPanelAdministrador --- se ejecuta");
    miFormulario = formulario.FormularioAcceder (request.form);
    if (request.method == 'POST'):
        print (miFormulario.correoElectronico.data);
        print (miFormulario.contrasena.data);
        if (miFormulario.correoElectronico.data == "jhon@gmail.com") and (miFormulario.contrasena.data == "james"):
            return redirect (url_for ('funcionAdministradorHome'));
    
    return (render_template("administradorlogin.html", miFormularioParametro = miFormulario));
    
@app.route('/administradorhome', methods = ['GET', 'POST'])   
def funcionAdministradorHome():
    return (render_template ("administradorhome.html"));

@app.route ('/administradorpanelrobot', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobot ():
	seHaIntentadoBorrar = request.args.get('seHaIntentadoBorrar', 'False') == 'True';
	seHaIntentadoModificar = request.args.get('seHaIntentadoModificar', 'False') == 'True';
	miListaRobots = Robot.query.all();

	return render_template ("administradorpanelrobot.html", miListaRobotsParametro=miListaRobots, seHaIntentadoBorrarParametro=seHaIntentadoBorrar, seHaIntentadoModificarParametro=seHaIntentadoModificar);

@app.route ('/adminstradorpanelrobotborrar/<int:idRobot>', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobotBorrar (idRobot):
	miRobot = Robot.query.filter_by (idRobot=idRobot).first();

	# en el caso de que ese robot este en servicio, No se puede elimiar ese robot. 
	if (miRobot.robotEnServicio == False):  # en el caso de que no este en servicio. 
		db.session.delete (miRobot);
		db.session.commit ();
	return redirect (url_for ('funcionAdministradorPanelRobot', seHaIntentadoBorrar=miRobot.robotEnServicio));

@app.route ('/administradorcrearrobot', methods = ['GET', 'POST'])
def funcionAdministradorCrearRobot ():
	miFormulario = formulario.FormularioCreaRobot (request.form);
	miFormulario.evento_idEvento.choices = [('-1', 'Este robot no se asigna a ningún evento.')]+ [(miEventoSeleccionado.idEvento, str(miEventoSeleccionado.idEvento)+ "- "+ miEventoSeleccionado.nombreDelEvento) for miEventoSeleccionado in Evento.query.all()]; 
	if (request.method == 'POST'): 
		eventoAlQuePerteneceraElRobot = None;
		if (int(miFormulario.evento_idEvento.data) != -1):
			eventoAlQuePerteneceraElRobot = miFormulario.evento_idEvento.data;
		miRobot = Robot (MACaddressDelRobot=miFormulario.MACaddressDelRobot.data, nombreDelRobot=miFormulario.nombreDelRobot.data, robotEnServicio=miFormulario.robotEnServicio.data, descripcionDelRobot=miFormulario.descripcionDelRobot.data, evento_idEvento=eventoAlQuePerteneceraElRobot);
		db.session.add (miRobot);
		db.session.commit();
		return redirect(url_for('funcionAdministradorPanelRobot'));

	return render_template ('administradorcrearrobot.html', miFormularioParametro = miFormulario, miParametroAccionHtml = "crear");

@app.route ('/adminstradorpanelrobotmodificar/<int:idRobot>', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobotModificar (idRobot):
	miFormulario = formulario.FormularioCreaRobot (request.form);
	miFormulario.evento_idEvento.choices = [('-1', 'Este robot no se asigna a ningún evento.')]+ [(miEventoSeleccionado.idEvento, str(miEventoSeleccionado.idEvento)+ "- "+ miEventoSeleccionado.nombreDelEvento) for miEventoSeleccionado in Evento.query.all()]; 
	miRobot = Robot.query.filter_by (idRobot=idRobot).first();

	# en el caso de que ese robot este en servicio, No se puede modificar ese robot. 
	if (miRobot.robotEnServicio == True):
		return redirect (url_for ('funcionAdministradorPanelRobot', seHaIntentadoModificar=miRobot.robotEnServicio));
	else:
		if (request.method == 'POST'):
			miRobot.MACaddressDelRobot = miFormulario.MACaddressDelRobot.data;
			miRobot.nombreDelRobot = miFormulario.nombreDelRobot.data;
			eventoAlQuePerteneceraElRobot = None;
			if (int(miFormulario.evento_idEvento.data) != -1):
				eventoAlQuePerteneceraElRobot = miFormulario.evento_idEvento.data;
			miRobot.evento_idEvento = eventoAlQuePerteneceraElRobot;
			miRobot.robotEnServicio = miFormulario.robotEnServicio.data;
			miRobot.descripcionDelRobot=miFormulario.descripcionDelRobot.data;
			db.session.commit();
			return redirect(url_for('funcionAdministradorPanelRobot'));	
	
		return render_template ("administradorcrearrobot.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar");

@app.route ('/adminstradorpanelrobotponerservicio/<int:idRobot>/<int:robotEnServicio>', methods = ['GET', 'POST'])
def funcionAdministradorPanelRobotPonerServicio (idRobot, robotEnServicio): 
	miRobot = Robot.query.filter_by (idRobot=idRobot).first();
	# en el caso de que el robot este en servicio y ademas tenga a un asistente dentro, lo que hago es eliminar ese asistente. 
	if (miRobot.robotEnServicio == True) and (miRobot.asistente_tokenDeSesion != None):  
		miRobot.asistente_tokenDeSesion = None;
	miRobot.robotEnServicio = bool (robotEnServicio);
	db.session.commit();
	return redirect (url_for ('funcionAdministradorPanelRobot'));

# en el caso de que se desactive el servicio, recordar eleimnar al aistente que este en la tabla, para que no pueda usar el robot. 


@app.route ('/administradorpanelevento', methods = ['GET', 'POST'])
def funcionAdministradorPanelEvento ():
	seHaIntentadoBorrar = request.args.get('seHaIntentadoBorrar', 'False') == 'True';  # esto es para el mensaje en de si ese evento que se ha pulsado en borrar se puede borrar o no. 
	seHaIntentadoModificar = request.args.get('seHaIntentadoModificar', 'False') == 'True';
	#print ("funcionAdministradorPanelEvento()---", seHaIntentadoBorrar);
	miLugarDelEventoNoEspecificado =  LugarDelEvento.query.filter_by (idLugarDelEvento=0).first();  # con esto lo que hago es crear una opcion en la que no se quiere especificar la calle del evento. 
	if (miLugarDelEventoNoEspecificado == None):
		miLugarDelEvento = LugarDelEvento (idLugarDelEvento=0, calle="No se espeficica la calle.", numero="No se especifica el número. ", codigoPostal=28001, edificioDondeSeCelebra="No se especificca el edificio donde se celebra.");
		db.session.add (miLugarDelEvento);
		db.session.commit();

	miListaEventos = Evento.query.all();
	return render_template ("administradorpanelevento.html", miListaEventosParametro=miListaEventos, seHaIntentadoBorrarParametro = seHaIntentadoBorrar, seHaIntentadoModificarParametro=seHaIntentadoModificar);

@app.route ('/administradorpaneleventoborrar/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdministradorPanelEventoBorrar (idEvento):
	#cuidado porque en esta parte en el caso de que el evento tenga robots, no se
	#puede borrar ese evento, porque sino los robots qquedarian que no se sabe de donde
	#son.   Para haccer esto, lo primero que hay que hacer es meterse en el panel de los
	# robots, y borrar a todos los robots del evento X que despues ya se puede borrar
	# con esta funcin que estoy haciendo. De manera que en esta funcon voy a tener qur
	# poner logica para que esto pase asi. 
	miEvento = Evento.query.filter_by (idEvento=idEvento).first();
	miLugarDelEvento = miEvento.lugarDelEvento_idLugarDelEvento;
	#print ("funcionAdministradorPanelEventoBorrar()---  este es el lugarDelEvento_idLugarDelEvento: ", miLugarDelEvento);
	variableQueDaElAvisoDeSiContieneRobotOAsistente = True;
	# print ("funcionAdministradorPanelEventoBorrar()--- cantidad de robots."  , len(miEvento.evento_idEvento_relacionRobot));
	if (miEvento) and (len(miEvento.evento_idEvento_relacionRobot) == 0) and (len(miEvento.evento_idEvento_relacionAsistente) == 0):
		variableQueDaElAvisoDeSiContieneRobotOAsistente = False;
		db.session.delete (miEvento);
		db.session.commit ();	
		# en esta parte una vez ya haya borrado ese Evento, voy a comprobar si no hay ningun evento que tenga como lugar a LugarDeEvento, que borre ese LugarDeEvento. 
		masEventosQueContenganEseLugar = Evento.query.filter_by (lugarDelEvento_idLugarDelEvento=miLugarDelEvento).first ();
		if (masEventosQueContenganEseLugar == None):
			print ("funcionAdministradorPanelEventoBorrar()--- no hay mas eventos que contengan ese lugar, se va a borrar el lugar. ");
			miObjetoLugarDelEvento = LugarDelEvento.query.filter_by (idLugarDelEvento=miLugarDelEvento).first();
			db.session.delete (miObjetoLugarDelEvento);
			db.session.commit ();
		
	return redirect (url_for ('funcionAdministradorPanelEvento', seHaIntentadoBorrar=variableQueDaElAvisoDeSiContieneRobotOAsistente));

@app.route ('/administradorcrearevento', methods = ['GET', 'POST'])
def funcionAdministradorCrearEvento ():
	miFormulario = formulario.FormularioCrearEvento (request.form);
	miFormulario.posiblesEventosAntiguos.choices = [('-1', 'No se va a seleccionar, tendrá que escribirlo')]+ [(miLugarSeleccionado.idLugarDelEvento, str(miLugarSeleccionado.idLugarDelEvento)+ "- "+ miLugarSeleccionado.calle+ " / "+ miLugarSeleccionado.numero+ " / "+ miLugarSeleccionado.edificioDondeSeCelebra) for miLugarSeleccionado in LugarDelEvento.query.all()]; 

	if (request.method == 'POST'):
		if (int(miFormulario.posiblesEventosAntiguos.data) >= 0): # en el caso de que se haya seleccionado un lugar del desplegable. De manera que la opcion "No se selecciona nada vale -1".
			#print ("funcionAdministradorEditarDatosEvento()--- ese lugar esta en la BBDD:  ", miFormulario.posiblesEventosAntiguos.data);
			miEvento = Evento (nombreDelEvento=miFormulario.nombreDelEvento.data, lugarDelEvento_idLugarDelEvento=miFormulario.posiblesEventosAntiguos.data);
			db.session.add (miEvento);
			db.session.commit();
		else:
			miLugarDelEvento = LugarDelEvento (calle=miFormulario.calleDelEvento.data, numero=miFormulario.numeroDelEvento.data, codigoPostal=miFormulario.codigoPostal.data, edificioDondeSeCelebra=miFormulario.edificioDondeSeCelebra.data);
			db.session.add (miLugarDelEvento);
			db.session.commit ();
			miEvento = Evento (nombreDelEvento=miFormulario.nombreDelEvento.data, lugarDelEvento_idLugarDelEvento=miLugarDelEvento.idLugarDelEvento);
			db.session.add (miEvento);
			db.session.commit();
		return redirect(url_for('funcionAdministradorPanelEvento'));

	return render_template ("administradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "crear");

@app.route ('/administradormodificardatosevento/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdministradorModificarDatosEvento (idEvento):
	miFormulario = formulario.FormularioCrearEvento (request.form);
	miFormulario.posiblesEventosAntiguos.choices = [('-1', 'No se va a seleccionar, tendrá que escribirlo')]+ [(miLugarSeleccionado.idLugarDelEvento, str(miLugarSeleccionado.idLugarDelEvento)+ "- "+ miLugarSeleccionado.calle+ " / "+ miLugarSeleccionado.numero+ " / "+ miLugarSeleccionado.edificioDondeSeCelebra) for miLugarSeleccionado in LugarDelEvento.query.all()];
	miEvento = Evento.query.filter_by (idEvento=idEvento).first();

	variableQueDaElAvisoDeSiContieneRobotOAsistente = False;  # esta parte es para controlar que en el caso de que un evento contenga asistentes, que no se le permita modificar.
	if (len (miEvento.evento_idEvento_relacionAsistente) > 0):
		variableQueDaElAvisoDeSiContieneRobotOAsistente = True;
		return redirect (url_for ('funcionAdministradorPanelEvento', seHaIntentadoModificar=variableQueDaElAvisoDeSiContieneRobotOAsistente));
	else: 
		if (request.method == 'POST'):  
			if (int(miFormulario.posiblesEventosAntiguos.data) >= 0): # este es el caso en el que se seleccione del desplegable. 
				miEvento.nombreDelEvento = miFormulario.nombreDelEvento.data;
				miEvento.lugarDelEvento_idLugarDelEvento=miFormulario.posiblesEventosAntiguos.data;
				db.session.commit();
			else:
				miLugarDelEvento = LugarDelEvento (calle=miFormulario.calleDelEvento.data, numero=miFormulario.numeroDelEvento.data, codigoPostal=miFormulario.codigoPostal.data, edificioDondeSeCelebra=miFormulario.edificioDondeSeCelebra.data);
				db.session.add (miLugarDelEvento);
				db.session.commit ();
				miEvento.nombreDelEvento = miFormulario.nombreDelEvento.data;
				miEvento.lugarDelEvento_idLugarDelEvento = miLugarDelEvento.idLugarDelEvento;
				db.session.commit();
		
				#aqui abria que borrar ese LugarDelEvento antiguo, pero antes comprobando si alguien nlo esta usando actualmente, que en este caso no se puede borrar. 
				miAntiguoLugarDelEvento = LugarDelEvento.query.filter_by (idLugarDelEvento=miEvento.lugarDelEvento_idLugarDelEvento).first();
				miOtroEventoQueTieneEseLugar = Evento.query.filter_by (lugarDelEvento_idLugarDelEvento=miAntiguoLugarDelEvento.idLugarDelEvento).first(); 
				if (miOtroEventoQueTieneEseLugar == None):  # en  el caso de que no haya otro Evento con ese LugarDelEvento, lo que hago es borrar ese LugarDelEvento. 
					if (miAntiguoLugarDelEvento.idLugarDelEvento != 0): # esto lo hago para no borrar el caso base que da la aopcion a que no se rellene el lugar. 
						db.session.delete (miAntiguoLugarDelEvento);
						db.session.commit ();
			return redirect(url_for('funcionAdministradorPanelEvento'));		

	return render_template ("administradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar");


if __name__ == '__main__':
	# esta es la manera nueva de obtener el certificado del csrf, ya que antes se llamaba con otra linea de codigo
	# este era la linea de codigo que se ponia al lado de los import:  csrf = CSRFProtect (app);
	csrf.init_app(app);

	# eto lo que hace es aplicar la configuracion de la base datos hecha en el archivo condig.py 
	db.init_app (app);

	# esto es para explicar bajo que contexto,  vamos a crear la DDBB.  (no lo entiendo bien)
	with app.app_context ():
	#esto se encarga de crear las tablas que no esten creadas en el modelo. 
		db.create_all ();

	#app.run(debug=True, port=8888);   Aqui tenia la configuracion inicial, recordar que esto ha pasado al archivo config.py
	# y por eso esta esta linea, app.run(debug=app.config['DEBUG'], port=app.config['PORT']);  Que consigue
	# el puerto y el modo debug, desde el archivo config.py. 
	app.run(debug=app.config['DEBUG'], port=app.config['PORT']);  

