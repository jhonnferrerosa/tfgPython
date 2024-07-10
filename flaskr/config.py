


import os
import psycopg2


class Config (object):
    SECRET_KEY = 'miPalabraSecreta';


# esta es la clase en la que vamos a hacer la configuracion para todo nuestro entorno de desarrollo. 
class DevelopmentConfig (Config):
    DEBUG = True;
    PORT=8888;
    SECRET_KEY = 'miPalabraSecreta';
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:esasFrasess11!!@localhost/baseDatosDemosRoboticas';
    

