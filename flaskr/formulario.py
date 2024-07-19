


from flask_wtf import Form
from wtforms import StringField
from wtforms.fields import EmailField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import BooleanField
from wtforms import FileField

from wtforms.validators import Length, InputRequired, NumberRange

class FormularioAcceder (Form):
	correoElectronico = EmailField('Introduzca su correo electronico:  (max. 50 caracteres): ', validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]); 
	contrasena  = StringField('Introduzca su contrasena (max. 50 caracteres): ', validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);

class FormularioCrearEvento (Form):
	nombreDelEvento = StringField ('Introdzca el nombre del evento (max. 50 caracteres): ', validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
	posiblesEventosAntiguos = SelectField ('Seleccione un lugar que esté actualemnte en el sistema: ', choices=[])
	calleDelEvento = StringField ('Introdzca la calle del evento (max. 50 caracteres): ', validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
	numeroDelEvento = StringField ('Introdzca el número de la calle del evento (max. 50 caracteres): ', validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
	codigoPostal = IntegerField ('Introdzca el código postal: ', validators=[NumberRange(min=10000, max=99999, message="El codigo postal debe de tener 5 dígitos.")]);
	edificioDondeSeCelebra = StringField ('Introdzca el edicifio donde se celebra el evento (max. 50 caracteres): ', validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
	
class FormularioCreaRobot (Form):
	MACaddressDelRobot = StringField ("Introoduzca la MAC del robot:  ", validators= [InputRequired("Esta campo es requerido"), Length(min=12, max=12, message="esciba entre 3 y 50 caracteres.")]);
	nombreDelRobot = StringField ("Introduzca el nombre del robot: ", validators= [InputRequired("Esta campo es requerido"), Length(min=3, max=50, message="esciba entre 3 y 50 caracteres.")]);
	evento_idEvento = SelectField ("Seleccione el evento en el que va a estar este robot: ", choices=[]);
	robotEnServicio = BooleanField ("Establezca si el robot esta listo para usarse: ");
	descripcionDelRobot = StringField ("Introduzca la descripcion del robot. ");
	fotoDelRobot = FileField ("Suba una foto del robot: ")



