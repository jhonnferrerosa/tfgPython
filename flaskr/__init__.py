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

import random

import os

# https://www.demosroboticas.com primera pagina para los asistentes. 
# https://www.demosroboticas.com/robotlisto
#  https://www.demosroboticas.com/esperando 


#  https://www.demosroboticas.com/adminstradorhome
#  https://www.demosroboticas.com/adminstradorpanelrobot
#  https://www.demosroboticas.com/adminstradordatosrobot

# https://www.demosroboticas.com/adminstradorcuentas
# https://www.demosroboticas.com/adminstradorpanelevento
#  https://www.demosroboticas.com/adminstradoreditardatosevento

app = Flask(__name__);  
app.config.from_object (DevelopmentConfig);

csrf = CSRFProtect ();

@app.before_request 
def miFuncionAntesDeLaPeticion (): 
	print  ("miFuncionAntesDeLaPeticion() --- este es el endpoint: ", request.endpoint); 

	if (request.endpoint == "funcionCierraNavegador"):
		print  ("miFuncionAntesDeLaPeticion() --- se va a eliminar en la BBDD: ", session.get('token'));
		if (session.get('token') != None):
			miToken = session.get('token');
			miAsistente = Asistente.query.filter_by (tokenDeSesion=miToken).first();
			if (miAsistente != None):   # ya que el endpoint de cerrar se llama varias veces, con el mismo token, lo que hago es que 
				# cuando ya no exista ese token, que no se borre otra vez porque sino no existe.  
				db.session.delete(miAsistente);
				db.session.commit();	


@app.route('/')   
def funcionIndex():
	if (('token' in session) == False):
		session['token'] = os.urandom(24).hex()  # Genera un token de sesión único
		miAsistente = Asistente (tokenDeSesion=session.get('token'), apodo="elChavo");
		db.session.add (miAsistente);
		db.session.commit();
		print ("funcionIndex()--- se ha crado el token.");
	else:
		print ("funcionIndex()--- ya existia una sesion: ", session.get('token'));
		# este es para el caso en el que ya se haya cerrado la sesion borrando en la base de datos, pero que se vuelva a 
		# abrir con el navegador la pagina web y le de el mismo token que el navegador recordaba antes, de manera que si 
		# no esta en la BBDD, lo que va a hacer es insertarlo otra vez. 
		if (Asistente.query.filter_by (tokenDeSesion=session.get('token')).first() == None):
			miAsistente = Asistente (tokenDeSesion=session.get('token'), apodo="elChavo");
			db.session.add (miAsistente);
			db.session.commit();
			print ("funcionIndex()--- ya existia una sesion y lo he vuelto a meter en la BBDD");
			
	return (render_template("index.html"));

@app.route('/robotlisto')
def functionRobotListo ():
	return (render_template("robotlisto.html"));

@app.route ('/esperando')
def funcionEsperando ():
	return render_template ("esperando.html");

@app.route ("/cierranavegador/", methods = ['POST'])
def funcionCierraNavegador ():
	return None;

@app.route('/adminstradorlogin', methods = ['GET', 'POST'])   
def funcionAdminstradorLogin():
    print ("funcionPanelAdminstrador --- se ejecuta");
    miFormulario = formulario.FormularioAcceder (request.form);
    if (request.method == 'POST'):
        print (miFormulario.correoElectronico.data);
        print (miFormulario.contrasena.data);
        if (miFormulario.correoElectronico.data == "jhon@gmail.com") and (miFormulario.contrasena.data == "james"):
            return redirect (url_for ('funcionAdminstradorHome'));
    
    return (render_template("adminstradorlogin.html", miFormularioParametro = miFormulario));
    
@app.route('/adminstradorhome', methods = ['GET', 'POST'])   
def funcionAdminstradorHome():
    return (render_template ("adminstradorhome.html"));

@app.route ('/adminstradorpanelevento', methods = ['GET', 'POST'])
def funcionAdminstradorPanelEvento ():
	seHaIntentadoBorrar = request.args.get('seHaIntentadoBorrar', 'False') == 'True'
	#print ("funcionAdminstradorPanelEvento()---", seHaIntentadoBorrar);

	miLugarDelEventoNoEspecificado =  LugarDelEvento.query.filter_by (idLugarDelEvento=0).first();  # con esto lo que hago es crear una opcion en la que no se quiere especificar la calle del evento. 
	if (miLugarDelEventoNoEspecificado == None):
		miLugarDelEvento = LugarDelEvento (idLugarDelEvento=0, calle="No se espeficica la calle.", numero="No se especifica el número. ", codigoPostal=28001, edificioDondeSeCelebra="No se especificca el edificio donde se celebra.");
		db.session.add (miLugarDelEvento);
		db.session.commit();

	miListaEventos = Evento.query.all();
	return render_template ("adminstradorpanelevento.html", miListaEventosParametro=miListaEventos, seHaIntentadoBorrarParametro = seHaIntentadoBorrar);

@app.route ('/adminstradorpaneleventoborrar/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdminstradorPanelEventoBorrar (idEvento):
	#cuidado porque en esta parte en el caso de que el evento tenga robots, no se
	#puede borrar ese evento, porque sino los robots qquedarian que no se sabe de donde
	#son.   Para haccer esto, lo primero que hay que hacer es meterse en el panel de los
	# robots, y borrar a todos los robots del evento X que despues ya se puede borrar
	# con esta funcin que estoy haciendo. De manera que en esta funcon voy a tener qur
	# poner logica para que esto pase asi. 
	miEvento = Evento.query.filter_by (idEvento=idEvento).first();
	miLugarDelEvento = miEvento.lugarDelEvento_idLugarDelEvento;
	#print ("funcionAdminstradorPanelEventoBorrar()---  este es el lugarDelEvento_idLugarDelEvento: ", miLugarDelEvento);
	variableQueDaElAvisoDeSiContieneRobotOAsistente = True;
	# print ("funcionAdminstradorPanelEventoBorrar()--- cantidad de robots."  , len(miEvento.evento_idEvento_relacionRobot));
	if (miEvento) and (len(miEvento.evento_idEvento_relacionRobot) == 0):
		variableQueDaElAvisoDeSiContieneRobotOAsistente = False;
		db.session.delete (miEvento);
		db.session.commit ();		
		# en esta parte una vez ya haya borrado ese Evento, voy a comprobar si no hay ningun evento que tenga como lugar a LugarDeEvento, que borre ese LugarDeEvento. 
		masEventosQueContenganEseLugar = Evento.query.filter_by (lugarDelEvento_idLugarDelEvento=miLugarDelEvento).first ();
		if (masEventosQueContenganEseLugar == None):
			print ("funcionAdminstradorPanelEventoBorrar()--- no hay mas eventos que contengan ese lugar, se va a borrar el lugar. ");
			miObjetoLugarDelEvento = LugarDelEvento.query.filter_by (idLugarDelEvento=miLugarDelEvento).first();
			db.session.delete (miObjetoLugarDelEvento);
			db.session.commit ();
		
	return redirect (url_for ('funcionAdminstradorPanelEvento', seHaIntentadoBorrar=variableQueDaElAvisoDeSiContieneRobotOAsistente));

@app.route ('/adminstradorcrearevento', methods = ['GET', 'POST'])
def funcionAdminstradorCrearEvento ():
	miFormulario = formulario.FormularioCrearEvento (request.form);
	miFormulario.posiblesEventosAntiguos.choices = [('-1', 'No se va a seleccionar, tendrá que escribirlo')]+ [(miLugarSeleccionado.idLugarDelEvento, str(miLugarSeleccionado.idLugarDelEvento)+ "- "+ miLugarSeleccionado.calle+ " / "+ miLugarSeleccionado.numero+ " / "+ miLugarSeleccionado.edificioDondeSeCelebra) for miLugarSeleccionado in LugarDelEvento.query.all()]; 

	if (request.method == 'POST'):
		if (int(miFormulario.posiblesEventosAntiguos.data) >= 0): # en el caso de que se haya seleccionado un lugar del desplegable. De manera que la opcion "No se selecciona nada vale -1".
			#print ("funcionAdminstradorEditarDatosEvento()--- ese lugar esta en la BBDD:  ", miFormulario.posiblesEventosAntiguos.data);
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
		return redirect(url_for('funcionAdminstradorPanelEvento'));

	return render_template ("adminstradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "crear");

@app.route ('/adminstradormodificardatosevento/<int:idEvento>', methods = ['GET', 'POST'])
def funcionAdminstradorModificarDatosEvento (idEvento):
	miFormulario = formulario.FormularioCrearEvento (request.form);
	miFormulario.posiblesEventosAntiguos.choices = [('-1', 'No se va a seleccionar, tendrá que escribirlo')]+ [(miLugarSeleccionado.idLugarDelEvento, str(miLugarSeleccionado.idLugarDelEvento)+ "- "+ miLugarSeleccionado.calle+ " / "+ miLugarSeleccionado.numero+ " / "+ miLugarSeleccionado.edificioDondeSeCelebra) for miLugarSeleccionado in LugarDelEvento.query.all()];
	miEvento = Evento.query.filter_by (idEvento=idEvento).first();

	if (request.method == 'POST'):  # este es el caso en el que se seleccione del desplegable. 
		if (int(miFormulario.posiblesEventosAntiguos.data) >= 0):
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
		return redirect(url_for('funcionAdminstradorPanelEvento'));		

	return render_template ("adminstradorcrearevento.html", miFormularioParametro = miFormulario, miParametroAccionHtml = "modificar");


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

