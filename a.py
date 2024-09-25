

## aqui lo que voy a poner es todo el codigo de pruebas, es decir las insercciones en BBDD que ya haya usado como ejeplo de pruebas y que no quiera dejar en el main.py
## para que si en algun momento quiero utilizar ese vodigo de pruebas, venir a este script y recuperarlo. 






#en esta parte voy a poner a los que no entran ya que incumplen alguno de los requisotos de la base de datos. 

@app.route ("/index3")   
def index3 ():
    miDisponibleRobot1 = DisponibleRobot (robot_idRobot=103, evento_idEvento = 3, fechaComienzoEnEvento='2024-09-01', fechaFinEnEvento='2024-09-30');  # este no entra, incimple requisito 4. 
    db.session.add (miDisponibleRobot1);
    db.session.commit ();
    return "<p>Hello, World! Demostraciones Robóticas.3 </p>";
    
@app.route ("/index3")   
def index3 ():
    miAsistente = Asistente (tokenDeSesion="ddd", evento_idEvento=1, robot_idRobot=101, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now()+timedelta(minutes=5)); #no entra, incumple requisito7. 
    db.session.add (miAsistente);
    db.session.commit ();
    return "<p>Hello, World! Demostraciones Robóticas.3 </p>";


    
@app.route ("/index3")   
def index3 ():
    miAsistente = Asistente (tokenDeSesion="ccc", evento_idEvento=1, robot_idRobot=106, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now()+timedelta(minutes=5)); #no entra, incumple requisito8. 
    db.session.add (miAsistente);
    db.session.commit ();
    return "<p>Hello, World! Demostraciones Robóticas.3 </p>";
    
@app.route ("/index3")   
def index3 ():
    miAsistente = Asistente (tokenDeSesion="ddd", evento_idEvento=1, robot_idRobot=105, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot=datetime.now()+timedelta(minutes=5)); #no entra, incumple requisito9. 
    db.session.add (miAsistente);
    db.session.commit ();
    return "<p>Hello, World! Demostraciones Robóticas.3 </p>";
    
@app.route ("/index3")   
def index3 ():
    miAsistente = Asistente (tokenDeSesion="ddd", evento_idEvento=1, robot_idRobot=106, fechaTomaDelRobot=datetime.now(), fechaAbandonoDelRobot='2024-11-30'); #no entra, incumple requisito9. 
    db.session.add (miAsistente);
    db.session.commit ();
    return "<p>Hello, World! Demostraciones Robóticas.3 </p>";
    
    
###### estos son pruebas para  probar algunas funciones que ejecuta la clase Administrador:  


@app.route ("/index3")     # esa la funcion:  funcion_crearRobot
def index3 ():
    
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miAdmin.funcion_crearRobot (110, "AABBCCDDddaa", "nombreAA");
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.3 </p>";


@app.route ("/index4")    #usa la fucnion: funcion_borrarRobot. 
def index4 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miAdmin.funcion_borrarRobot (110);
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.4 </p>";

@app.route ("/index5")   # usa la funcion:  funcion_modificarRobot. 
def index5 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miAdmin.funcion_borrarRobot (110);
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.4 </p>";
    
@app.route ("/index6")     # usa la funcion:  funcion_modificarRobot. 
def index6 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miAdmin.funcion_modificarRobot (110, 120, "cafe0000cafe", "robotcafe.");
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.6 </p>";
    
    
@app.route ("/index7")   
def index7 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miAdmin.funcion_activarOdesactivarRobot (110, False);
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.7 </p>";
    
    
@app.route ("/index8")   
def index8 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miPila = [];
        elemento1 = [1, 130, '2024-09-01', '2024-09-30'];
        elemento2 = [1, 131, '2024-09-01', '2024-09-30'];
        elemento3 = [1, 132, '2024-09-01', '2024-09-30'];
        miPila.append (elemento1);
        miPila.append (elemento2);
        miPila.append (elemento3);
        miAdmin.funcion_crearEvento (miPila, 5, "eurobot", "calle EPS");
        
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.8 </p>";
    
    
@app.route ("/index9")   
def index9 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miPila = [];
        elemento1 = [1, 130, '2024-09-01', '2024-09-30'];
        elemento2 = [1, 131, '2024-09-01', '2024-09-30'];
        elemento3 = [1, 132, '2024-09-01', '2024-09-30'];
        miPila.append (elemento1);
        miPila.append (elemento2);
        miPila.append (elemento3);
        miAdmin.funcion_crearEvento (miPila, 5, "eurobot", "calle EPS");
        
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.9 </p>";
    
@app.route ("/index10")   
def index10 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miAdmin.funcion_modificarDatosDelEvento (1, 10, "aula2025", "calleIFEMA25");
        
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.10 </p>";
    
@app.route ("/index11")   
def index11 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");

        miEvento_idEvento = 1;
        miRobot_idRobot = 132;
        miFechaComienzoEnEvento = '2024-09-01';
        miFechaFinEnEveto = '2024-09-30';
        
        miNuevaFechaComienzoEnEvento = '2024-10-01';
        miNuevaFechaFinEnEvento = '2024-10-30'
        
        miAdmin.funcion_modificarRobotsDelEvento (miEvento_idEvento, miRobot_idRobot, miFechaComienzoEnEvento, miFechaFinEnEveto, miNuevaFechaComienzoEnEvento, miNuevaFechaFinEnEvento);
        
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.11 </p>";
    
    
@app.route ("/index12")   
def index12 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
    
        miAdmin.funcion_borrarEvento (2);

    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.12 </p>";
    
@app.route ("/index13")   
def index13 ():
    miCorreoAdmin = ("jhon@gmail.com");
    miAdmin = Administrador.query.filter_by (_Administrador__correoElectronico=miCorreoAdmin).first ();
    if (miAdmin):
        print ("se ha encontrado el administradior. ");
        miEvento_idEvento = 1;
        miRobot_idRobot = 132;
        miFechaComienzoEnEvento = '2024-09-01';
        miFechaFinEnEveto = '2024-09-30';miListaDisponibleRobot
        miAdmin.funcion_borrarRobotDelEvento (miEvento_idEvento, miRobot_idRobot, miFechaComienzoEnEvento, miFechaFinEnEveto);
    else:
        print ("No se ha encontrado el adminstrador. ");
    return "<p>Hello, World! Demostraciones Robóticas.13 </p>";
    
    
    

    

    
    
    
    
    


