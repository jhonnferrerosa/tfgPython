

## aqui lo que voy a poner es todo el codigo de pruebas, es decir las insercciones en BBDD que ya haya usado como ejeplo de pruebas y que no quiera dejar en el main.py
## para que si en algun momento quiero utilizar ese vodigo de pruebas, venir a este script y recuperarlo. 




#Esta no va a entrar.  este me vale para comprobar que funciona el indice GIST en la relacion disponibleRobot, ya que en todo noviembre ya hay un robot funcionando. 
@app.route ("/index5")
def index5 ():
    miDisponibleRobot1 = DisponibleRobot (eventos_nombreDelEvento="aula1", eventos_fechaDeCreacionDelEvento="2024-10-01", eventos_lugarDondeSeCelebra="ifema1", robots_idRobot=101 , fechaComienzoEnEvento="2024-11-01", fechaFinEnEvento="2024-11-30");
    db.session.add (miDisponibleRobot1);
    db.session.commit ();
    return "<p> este es el index5.  </p>";



# este no entra. lo que esta pasando es que ese robot ya esta ocupad oen todo noveembre, y lo estoy intentndo controlar con otro asistentes en esa misma fecha. 
@app.route ("/index5")
def index5 ():
    miControla1 = Controla (asistentes_identificadorUnicoAsistente="IUA2", robots_idRobot=101, fechaTomaDelRobot="2024-11-01", fechaAbandonoDelRobot="2024-11-30");
    db.session.add (miControla1);
    db.session.commit ();
    return "<p> este es el index5.  </p>";

# este no entra, ya que el asistente IUA1 ya controla un robot en todo noviembre, no puede controlar mas robots en noviembre. 
@app.route ("/index5")
def index5 ():
    miControla = Controla (asistentes_identificadorUnicoAsistente="IUA1", robots_idRobot=102, fechaTomaDelRobot="2024-11-01", fechaAbandonoDelRobot="2024-11-30");
    db.session.add (miControla);
    db.session.commit ();
    return "<p> este es el index5.  </p>";


#  estas insercciones en la tabla COntrola, sí que valen, pero antes de crear el trigger, porque despues de que se cree el trigger dde la tabla Controla, esto ya no vale para nada. Y es que lo que pasa es que el trigger comprueba  que ese robot que se pasa a 
# controlar por parte de ese asistente, que el evento en el que este el asistente, sea el que se corresponde con el que esta el robot en ese momento.  Por lo tanto, esto sólo me vala para commprobar que  en la tabla controla, no salte la exception por el indice
# GIST , con esa fecha de toma y de abandono.  
    miControla1 = Controla (asistentes_identificadorUnicoAsistente="IUA1", robots_idRobot=101, fechaTomaDelRobot="2024-11-01", fechaAbandonoDelRobot="2024-11-30");
    miControla2 = Controla (asistentes_identificadorUnicoAsistente="IUA2", robots_idRobot=101, fechaTomaDelRobot="2024-12-01", fechaAbandonoDelRobot="2024-12-30");
    miControla3 = Controla (asistentes_identificadorUnicoAsistente="IUA1", robots_idRobot=102, fechaTomaDelRobot="2024-12-01", fechaAbandonoDelRobot="2024-12-30");
    db.session.add (miControla1);
    db.session.add (miControla2);
    db.session.add (miControla3);
    db.session.commit ();



# para robar esta:  raise Exception ("exception.B_I. Ese robot no esta en ningun evento.");
@app.route ("/index5")
def index5 ():
    miControla = Controla (asistentes_identificadorUnicoAsistente="IUA3", robots_idRobot=103, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now() + timedelta(minutes=5));
    db.session.add (miControla);
    db.session.commit ();
    return "<p> este es el index5.  </p>";

# para probar este:    raise Exception ("exception.B_I. Ese asistente, no está en ese evento en el cual se ha solicitado ese robot. ");
@app.route ("/index6")
def index6 ():
    miControla = Controla (asistentes_identificadorUnicoAsistente="IUA4", robots_idRobot=104, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now() + timedelta(minutes=5));
    db.session.add (miControla);
    db.session.commit ();
    return "<p>  este es el index 6";


# probar que salta este execotion:  raise Exception ("exception.B_I. Ese robot y ese asistente, sí etan en ese evento, pero le fecha en la que ta el robot en el evento, no abarca la fecha en la que ese asistente maneja ese robot. ");
# me lo da este codigo:   
@app.route ("/index7")
def index7 ():

    miControla = Controla (asistentes_identificadorUnicoAsistente="IUA3", robots_idRobot=104, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now() + timedelta(days=30));
    db.session.add (miControla);
    db.session.commit ();
    return "<p>  este es el index 7";




    
    

    

    
    
    
    
    


