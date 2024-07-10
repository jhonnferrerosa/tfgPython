


from flask_wtf import Form
from wtforms import StringField
from wtforms.fields import EmailField
from wtforms import IntegerField
from wtforms import DateField
from wtforms import SelectField

from wtforms import validators

class FormularioAcceder (Form):
	correoElectronico = EmailField('Introduzca su correo electronico:  (max. 50 caracteres): ', [validators.length(min=1, max=50, message="tiene que se un corrreo. ")]); 
	contrasena  = StringField('Introduzca su contrasena (max. 50 caracteres): ', [validators.length(min=1, max=50, message="maximo 50 caracteres.")]);

class FormularioCrearEvento (Form):
	nombreDelEvento = StringField ('Introdzca el nombre del evento (max. 50 caracteres): ', [validators.length(min=1, max=50, message="maximo 50 caracteres.")]);
	posiblesEventosAntiguos = SelectField ('Seleccione un lugar que esté actualemnte en el sistema: ', choices=[])
	calleDelEvento = StringField ('Introdzca la calle del evento (max. 50 caracteres): ', [validators.length(min=1, max=50, message="maximo 50 caracteres.")]);
	numeroDelEvento = StringField ('Introdzca el número de la calle del evento (max. 50 caracteres): ', [validators.length(min=1, max=50, message="maximo 50 caracteres.")]);
	codigoPostal = IntegerField ('Introdzca el código postal: ');
	edificioDondeSeCelebra = StringField ('Introdzca el edicifio donde se celebra el evento (max. 50 caracteres): ', [validators.length(min=1, max=50, message="maximo 50 caracteres.")]);
	



