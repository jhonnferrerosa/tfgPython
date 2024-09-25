
from datetime import datetime

# en esta lista voy a alamecenar todos los robots que no estan en servicio, para que cuando se haga la consulta de conseguir robots de un evento, me va a devolver los robots del evento, pero sin saber cual de ellos es el que está en servicio, porque 
#recoordar que esto no lo puedo guardar en la BBDD.
miListaRobotsQueNoEstanEnServicio = [];

# en este diccionario voy a almacenar  como clave al idEvento de los eventos para que no se pueda repetir evento, por lo tanto para cada clave, el valor va a ser una lista de token que son los asistentes.
miDiccionarioEventoYasistentesDatos = {}
