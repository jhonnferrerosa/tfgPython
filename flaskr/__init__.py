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

miDiccionarioGloalTokensEnteros = {};
miDiccionarioGloalTokensBoolPorPrimerAcceso = {};
miDiccionarioGlobalTokensListaDeRobotsRechazados = {};

def funcionEliminaAsistenteDeLaBaseDeDatos (tokenDeSesion):
	time.sleep (10);
	print ("funcionEliminaAsistenteDeLaBaseDeDatos()--- ese token: ", tokenDeSesion, " tiene estos intentos: ", miDiccionarioGloalTokensEnteros[tokenDeSesion]);
	if (miDiccionarioGloalTokensEnteros[tokenDeSesion] == 0):  # en este caso si que puedo borrar de la BBDD. 
		miAsistente = Asistente.query.filter_by (tokenDeSesion=tokenDeSesion).first();
		if (miAsistente != None): # esto lo hago para ahorrarme el problema de que si por algun casual se intenta borrar varias veces, que la web no de error de integridad. 
			db.session.delete(miAsistente);
			db.session.commit();	
			miRobot = Robot.query.filter_by (asistente_tokenDeSesion=tokenDeSesion).first();
			if (miRobot != None):
				print ("funcionEliminaAsistenteDeLaBaseDeDatos()--- ese asistente esta en un robot, lo quito del robot. ");
				miRobot.asistente_tokenDeSesion = None;
			# to do: aqui deberia de poner otro if mas que diga que en el caso dee que se borre de BBDD, que tambien se borre del diccionario. 
	else:
		miDiccionarioGloalTokensEnteros[tokenDeSesion] -= 1;

@app.before_request 
def miFuncionAntesDeLaPeticion (): 
	global miDiccionarioGloalTokensBoolPorPrimerAcceso;
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
		miDiccionarioGloalTokensEnteros[session.get('token')] = 0;  # establezco que ese token tien cero intentos de poder ser borrado por la funcionCierraNavegador en @app.before_request
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
			miDiccionarioGloalTokensEnteros[session.get('token')] = 0;  # establezco que ese token tien cero intentos de poder ser borrado por la funcionCierraNavegador en @app.before_request
			miAsistente = Asistente (tokenDeSesion=session.get('token'), apodo="elChavo", evento_idEvento=5, fechaDeAccesoAlSistema=datetime.now());
			db.session.add (miAsistente);
			db.session.commit();
			print ("funcionIndex()--- ya existia una sesion y lo he vuelto a meter en la BBDD");
		else:
			print ("funcionIndex()---Si esta en BBDD y este es el tamaño del diccionario, es decir cantidad de navegadores: ", len (miDiccionarioGloalTokensEnteros));
			# esto es para el caso de que se cierre la aplciacion y se borre el diccionario con los tokens activos. De esta manera que no caiga en error en el caso de 
			# que hay un token que si que existe (segun lo que dice el navegador) pero que luego en mi lista de diccionario no esta. 
			if ((session.get('token') in miDiccionarioGloalTokensEnteros) == False):
				print ("funcionIndex()--- ese token existe en la BBDD, pero no en el diccionario");
				miDiccionarioGloalTokensEnteros[session.get('token')] = 0;
			else: 
				print ("funcionIndex()--- ese token esta en el diccionario. ");
				miDiccionarioGloalTokensEnteros[session.get('token')] += 1;


	# esto es para el caso en el que ya se haya hecho una seleccion de robots rechazados, por tanto ya hay diccionario. Para no restablecerlo, ya que puede ser que una
	#  vez que se haya rechazado a ciertos robots, que se intente volver al index para que se borren todos estos robots rechazados, de esta manera en el caso de que
	# alguien haga la trampa de rescribir el endpiont, que no se le borren los robots rechazados. 
	if ((session.get('token') in miDiccionarioGlobalTokensListaDeRobotsRechazados) == False): 
		miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')] = [];
		
	# para este caso el diccionario miDiccionarioGlobalTokensListaDeRobotsRechazados  ya existe, lo que puede indicar que ya se ha accedido a algun robot. 
	# asi que lo que hago es comprobar si estoy en uno, y si lo estoy, lo mando a la pantalla donde informa al sistente que lo esta controlado.
	miRobot = Robot.query.filter_by (asistente_tokenDeSesion = session.get('token')).first();
	if (miRobot != None):
		miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = True;
		return redirect (url_for ("functionRobotListo", idRobot=miRobot.idRobot, robotaceptado=True));
	return (render_template("index.html"));

@app.route ('/ponerseAlaColaDeControlarUnRobot')
def functionPonerseAlaColaDeControlarUnRobot ():
	global miDiccionarioGloalTokensEnteros;
	global miDiccionarioGloalTokensBoolPorPrimerAcceso;
	global miDiccionarioGlobalTokensListaDeRobotsRechazados;

	if (session.get('token') == None) or (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None) or ((session.get('token') in miDiccionarioGloalTokensEnteros) == False): 
		return redirect (url_for ('funcionIndex'));
	else:
		miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = True;
		# esto se cambiar por un blucle for y devolver lo mismi, miRobot, en el caso de que haya alguno. 
		misRobots = Robot.query.filter (Robot.robotEnServicio==True, Robot.asistente_tokenDeSesion==None).all();
		miRobot = None;
		for indiceRobot in misRobots:
			if ((indiceRobot.idRobot in miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')]) == False):  # en el caso de que el robot de indice i no este en la lista. 
				miRobot = indiceRobot;
				break;
		if (miRobot): #si hay robots. 
			print ("functionPonerseAlaColaDeControlarUnRobot()--- si hay robot, este es su ID: ", miRobot.idRobot);
			return redirect (url_for ("functionRobotListo", idRobot=miRobot.idRobot));
		else: 	
			print ("functionPonerseAlaColaDeControlarUnRobot()---  No hay robots. ");
			return redirect (url_for ("funcionEsperando"));


@app.route('/robotlisto/<int:idRobot>')
@app.route('/robotlisto/<int:idRobot>/<int:robotaceptado>')
def functionRobotListo (idRobot, robotaceptado = False):
	global miDiccionarioGloalTokensEnteros; 
	global miDiccionarioGloalTokensBoolPorPrimerAcceso;
	if (session.get('token') == None) or (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None) or ((session.get('token') in miDiccionarioGloalTokensEnteros) == False): 
		return redirect (url_for ('funcionIndex'));
	else:
		if (miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] == True): 
			print ("functionRobotListo()--- se abre la pagina debido a un redirect. ");
			miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = False;
		else:
			print ("functionRobotListo()--- se abre la pagina debido a una recarga. ");
			miDiccionarioGloalTokensEnteros[session.get('token')] += 1;
		if (robotaceptado == False):
			miRobot = Robot.query.filter_by (idRobot=idRobot).first();
			return (render_template("robotlisto.html", miRobotParametro=miRobot, miParametroRobotaceptado=robotaceptado));
		else:
			miRobot = Robot.query.filter_by (idRobot=idRobot).first();
			return (render_template("robotlisto.html", miRobotParametro=miRobot, miParametroRobotaceptado=robotaceptado));


@app.route ('/esperando')
def funcionEsperando ():
	global miDiccionarioGloalTokensEnteros; 
	global miDiccionarioGloalTokensBoolPorPrimerAcceso;
	global miDiccionarioGlobalTokensListaDeRobotsRechazados;
	 # en el caso de que no tenga token de sesion que se vuelva al index a obtenerlo. o en el caso de que la sesion no este en la base
	 # de datos tambien mandarlo al index para que la ponga en la BBDD. O en el caso de que ese token no este en el diccionario mandarlo
	 # al index. 
	if (session.get('token') == None) or (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None) or ((session.get('token') in miDiccionarioGloalTokensEnteros) == False): 
		print ("funcionEsperando()--- no existe el token O no esta en la BBDD O no esta en el diccionario. ");
		return redirect (url_for ('funcionIndex'));
	else:
		if (miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] == True): 
			print ("funcionEsperando()--- se abre la pagina debido a un redirect. ");
			miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = False;
		else: 
			print ("funcionEsperando()--- se abre la pagina debido a una recarga. ");
			miDiccionarioGloalTokensEnteros[session.get('token')] += 1;
		misRobots = Robot.query.filter (Robot.robotEnServicio==True, Robot.asistente_tokenDeSesion==None).all();
		miRobot = None;
		for indiceRobot in misRobots:
			if ((indiceRobot.idRobot in miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')]) == False): 
				print ("funcionEsperando()--- ese robot no esta en la lista de recahzados");
				miRobot = indiceRobot;
				break;
			else:
				print ("funcionEsperando()--- ese robot SI esta en la lista de recahzados");

		if (miRobot): #si hay robots. 
			print ("funcionEsperando()---  si hay robot, este es su ID: ", miRobot.idRobot);
			print ("funcionEsperando()--- se va a hacer la redireccion. ");
			miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = True;
			return redirect (url_for ("functionRobotListo", idRobot=miRobot.idRobot));
	miListaRobots = Robot.query.all();
	return render_template ("esperando.html", miListaRobotsParametro=miListaRobots);


@app.route ('/rechazarrobot/<int:idRobot>')
def funcionRechazarRobot (idRobot):
	global miDiccionarioGloalTokensEnteros;
	global miDiccionarioGloalTokensBoolPorPrimerAcceso;
	global miDiccionarioGlobalTokensListaDeRobotsRechazados;

	if (session.get('token') == None) or (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None) or ((session.get('token') in miDiccionarioGloalTokensEnteros) == False): 
		return redirect (url_for ('funcionIndex'));
	else:
		miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = True;
		miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')].append (idRobot);
		print ("funcionRechazarRobot()--- este es el robot rechazado:  ",idRobot);
		misRobots = Robot.query.filter (Robot.robotEnServicio==True).all();
		miVariableTodaviaHayRobotsNoRechazadosEnLaBBDD = False;
		for indiceRobot in misRobots: 
			if ((indiceRobot.idRobot in miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')]) == False): # esto es que todavia hay algun robot que no se ha rechazado. 
				miVariableTodaviaHayRobotsNoRechazadosEnLaBBDD = True;
				print ("funcionRechazarRobot()--- todavia hay robots que no estan rechazados");
				break;
		if (miVariableTodaviaHayRobotsNoRechazadosEnLaBBDD == False):
			miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')] = [];
			print ("funcionRechazarRobot()--- se han rechazado todos los robots, se restablece a que no hay robots rechazados. ");

		return redirect (url_for ('funcionEsperando'));

@app.route ('/aceptarrobot/<int:idRobot>')
def funcionAceptarRobot (idRobot):
	global miDiccionarioGloalTokensEnteros;
	global miDiccionarioGloalTokensBoolPorPrimerAcceso;
	global miDiccionarioGlobalTokensListaDeRobotsRechazados;

	if (session.get('token') == None) or (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None) or ((session.get('token') in miDiccionarioGloalTokensEnteros) == False): 
		return redirect (url_for ('funcionIndex'));
	else:
		miDiccionarioGloalTokensBoolPorPrimerAcceso[session.get('token')] = True;
		miDiccionarioGlobalTokensListaDeRobotsRechazados[session.get('token')] = [];
		miRobot = Robot.query.filter_by (idRobot=idRobot).first();
		miRobot.asistente_tokenDeSesion = session.get('token');
		db.session.commit();
		return redirect (url_for ("functionRobotListo", idRobot=miRobot.idRobot, robotaceptado=True));



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

