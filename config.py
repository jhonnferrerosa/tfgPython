





import psycopg2

# esta es la clase en la que vamos a hacer la configuracion para todo nuestro entorno de desarrollo. 
class DevelopmentConfig ():
    DEBUG = True;
    PORT=5000;
    SECRET_KEY = 'miPalabraSecreta';  # esto hasta que no use un formulario con csrf token, no lo puedo usar.  Mirar si esto se puede sacar del sistema operativo ya que es una clave que tiene que estar segura.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Grandesvirus2!@localhost/z';

    




