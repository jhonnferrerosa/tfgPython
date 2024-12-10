
from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField, FileField, HiddenField, PasswordField, BooleanField, TextAreaField, validators, SelectField
from wtforms.fields import EmailField

# esto me vale para utilizar expresiones regulares en pyrhon. 
import re


from wtforms.validators import Length, InputRequired, NumberRange, MacAddress, URL, Optional

class FormularioAcceder (Form):
    """
        Este formulario lo utilizo para el login y el signup, para el administrador. 
    """
    correoElectronico = EmailField(validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]); 
    contrasena  = PasswordField(validators= [Optional(), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    confirmarContrasena  = PasswordField(validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    opcionMostrarContrasena = BooleanField('Mostrar contraseña');
            

class FormularioCreaRobot (Form):
    """ 
        Este formulario lo uso para crear y modificar un robot en el sistema. 
    """
    macAddressDelRobot = StringField (validators= [InputRequired("Esta campo MAC es requerido"), Length(min=17, max=17), MacAddress("Debe de introducir una MAC correcta, los caracteres deben ser hexagesimal, y el formato debe ser XX:XX:XX:XX:XX:XX")]);
    nombreDelRobot = StringField (validators= [InputRequired("Esta campon nombre es requerido"), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    descripcionDelRobot = TextAreaField  (validators=[Optional(), Length(max=100, message="Escriba entre 3 y 100 caracteres")]);
    fotoDelRobot = FileField();

class FormularioCrearEvento (Form):
    """ 
        Este formulario lo uso para crear y modificar un evento en el sistema. 
    """
    nombreDelEvento = StringField (validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    fechaDeCreacionDelEvento = HiddenField ();
    lugarDondeSeCelebra = StringField (validators= [Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    codigoQR = StringField ();
    calle = StringField (validators= [Optional(), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    numero = StringField (validators= [Optional(), Length(min=3, max=50, message="Esciba entre 3 y 50 caracteres.")]);
    codigoPostal = IntegerField (validators=[Optional(), NumberRange(min=10000, max=99999, message="El codigo postal debe de tener 5 dígitos.")]);

    # en este caso, solo que con que el nombre de la funcion tenga este nombre validate_codigoQR ya sé que se está refiriendo al campo codigoQR del formulario. 
    def validate_codigoQR (form, field):
        miCampoCodigoQR = field.data;
        if (miCampoCodigoQR != "") and (miCampoCodigoQR != None):
            miExpresionRegular = r"^[a-zA-Z0-9@.:\-]+$";
            miVerdadCodigoQRvalidado = bool (re.match (miExpresionRegular, miCampoCodigoQR));
            if (miVerdadCodigoQRvalidado == False):
                raise validators.ValidationError ("Sólo se permite caracteres alfanuméricos en la URL. No vale espacios ni carecteres especiales "); 

class FormularioBuscarRobot (Form):
    """
        Este formulario lo uso como buscador de robots. 
    """
    # este valor:  render_kw,  hace que en el caso de que se pase un atributo valido  (como por ejemplo, style o placeholder) junto con un valor correcto (background-color: black) entonces hace que se aplique ese estilo.  
    # campoBuscadorRobotString = StringField (validators= [InputRequired("Esta campo es requerido"), Length(max=50, message="Esciba entre 3 y 50 caracteres.")], render_kw={"placeholder": "Robot explorador"});
    campoBuscadorRobotString = StringField (validators= [InputRequired("Esta campo es requerido"), Length(max=50, message="Esciba entre 3 y 50 caracteres.")]);
    campoBuscadorRobotSelect = SelectField (choices=[]);

class FormularioBuscarEvento (Form):
    """
        Este formulario lo uso como buscador de eventos. 
    """
    campoBuscadorEventoString = StringField (validators= [InputRequired("Esta campo es requerido"), Length(max=50, message="Esciba entre 3 y 50 caracteres.")]);
    campoBuscadorEventoSelect = SelectField (choices=[]);








