
from flask_wtf import Form

# SelectField, es para esto: evento_idEvento = SelectField ("Seleccione el evento en el que va a estar este robot: ", choices=[]);

from wtforms import StringField, IntegerField, SelectField, BooleanField, FileField, DateTimeField, HiddenField, PasswordField, BooleanField
from wtforms.fields import EmailField


from wtforms.validators import Length, InputRequired, NumberRange, MacAddress

class FormularioAcceder (Form):
    """
        Este formulario lo utilizo para el login y el signup, para el administrador. 
    """
    correoElectronico = EmailField(validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]); 
    contrasena  = PasswordField(validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    confirmarContrasena  = PasswordField(validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    opcionMostrarContrasena = BooleanField('Mostrar contraseña');

class FormularioCreaRobot (Form):
    """
        Este formulario lo uso para crear y modificar un robot en el sistema. 
    """
    macAddressDelRobot = StringField (validators= [InputRequired("Esta campo es requerido"), Length(min=17, max=17), MacAddress("Debe de introducir una MAC correcta, los caracteres deben ser hexagesimal, y el formato debe ser XX:XX:XX:XX:XX:XX")]);
    nombreDelRobot = StringField (validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    descripcionDelRobot = StringField ();
    fotoDelRobot = FileField();
    

class FormularioCrearEvento (Form):
    """ 
        Este formulario lo uso para crear y modificar un evento en el sistema. 
    """
    idEvento = IntegerField (validators=[NumberRange(min=1, max=99999, message="El id del evento tiene que ser mayor que cero y como máximo 5 dígitos.")]);
    nombreDelEvento = StringField (validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    calle = StringField (validators= [Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    numero = StringField (validators= [Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    codigoPostal = IntegerField (validators=[NumberRange(min=1000, max=99999, message="El codigo postal debe de tener 5 dígitos.")]);
    edificioDondeSeCelebra = StringField (validators= [Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
    
class FormularioModificarFechasRobot (Form):
    """
        Este formulario lo uso para modificar la tabla disponibleRobot, y es que con la fecha de comienzo la paso rellena para que el cliente vea que fecha 
        actualmente va a ser o esta siendo usado el robot por parte de ese evento. Por otro lado con la fecha antigua lo que estoy haciendo es pasarsela al 
        cliente para que luego la devuelva y de esta forma yo pueda tener la fecha antigua y la nueva, para posteriormente meterla en la funcion que 
        modifica esa fecha.  
    """
    fechaComienzoEnEvento = DateTimeField (format='%Y-%m-%d %H:%M:');
    fechaFinEnEvento = DateTimeField (format='%Y-%m-%d %H:%M:');
    robot_idRobot = HiddenField ();
    fechaComienzoEnEventoAntigua = HiddenField ();
    fechaFinEnEventoAntigua = HiddenField ();


    
    


    
    
    






