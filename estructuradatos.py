
# en esta lista voy a almacenar todos los robots que no estan en servicio, para que cuando se haga la consulta de conseguir robots de un evento, me va a devolver 
# los robots del evento, y junto con esta lista, consigo los que estan en un evento, pero que no estan en servicio, y esos son los que puede utilizar el asistente. 
miListaRobotsQueNoEstanEnServicio = [];

# en este diccionario voy a almacenar  como clave al idEvento de los eventos para que no se pueda repetir evento, por lo tanto para cada clave, el valor va a ser
#  una lista de token que son los asistentes.
miDiccionarioEventoYasistentesDatos = {};
