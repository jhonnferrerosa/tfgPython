
import os

from dotenv import load_dotenv

load_dotenv()

# esta es la clase en la que vamos a hacer la configuracion para todo nuestro entorno de desarrollo. 
class DevelopmentConfig ():
    DEBUG = True;
    PORT=5000;
    #SECRET_KEY = 'miPalabraSecreta';  # esto hasta que no use un formulario con csrf token, no lo puedo usar.  Mirar si esto se puede sacar del sistema operativo ya que es una clave que tiene que estar segura.
    SECRET_KEY = os.getenv ('SECRET_KEY');
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Grandesvirus2!@localhost/z';  
    MAIL_SERVER = 'smtp.gmail.com';
    MAIL_PORT = 587;
    MAIL_USE_SSL = False;
    MAIL_USE_TLS = True;
    MAIL_USERNAME = "jhonn.uah.trabajofindegrado@gmail.com";
    # en esta parte, no es la contrasña del correo, sino que es la contraseña que se genera en este LINK, teniendo abierto en ese navegador el correo que se quiere utilizar:
    #  https://www.google.com/account/about/?hl=es-419&utm_source=google-account&utm_medium=web
    MAIL_PASSWORD = "unag cpvo rcxt ifst";


    