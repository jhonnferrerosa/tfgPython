
// en esta funcion cnado me refiero al campo addEventListener de macAddresDelRobot,  lo que permite es que cuando se escriba una MAC y se escriba un caracter que no es hexagesimal, 
//que salga un mesaje de error diciendo que se ha escrito mal la MAC.
// lo que hace tambien es que en el caso de que se escriba un caracter en minuscula, que se pase a mayuscula. 
// y ademas en el caso de que se este escribiendo bien la MAC, entonces que los dos puntos se escriban solos. 

//cuando me refiero al addEventListener del boton de enviar botonEniarId, lo que hago primero es comprobar que la MAC tanga los 17 caracteres. 
// y en el caso de que los tenga, lo que hago es comprobar el formato de la MAC, para validarlo antes de enviarselo al servidor. 

function validarMac (){
	let miMacAddressDelRobotAnterior = null;
	let miMacAddressDelRobot = document.getElementById ("macAddressDelRobot");
	miMacAddressDelRobot.addEventListener ("input", function (event){
			// en el caso de que sea suprimir o delete, no se tiene encuenta el alert, es decir, dentro de la expresion regular, estoy añadendo los botones de borrado. 
			if (event.data != null){
				// en el caso de que haya escrito un caracter incorrecto, devuelve true la expresion regular. En ese caso el caracter entonces no vale. 
				if (/[^0-9a-fA-F:]/.test(event.data)){
					alert ("caracter incorrecto para una MAC address");
					miMacAddressDelRobot.value = miMacAddressDelRobotAnterior;
				}else{
					// en el caso de que se detecte una minuscula dentro del String que se acaba de escribir, lo que hago es que el valor de la MAC lo  paso a mayuscula.
					for (let i = 0; i < event.data.length; i++){
						if ((event.data[i] >= 'a') && (event.data[i] <= 'z')){
							miMacAddressDelRobot.value = miMacAddressDelRobot.value.toUpperCase ();
							// este break lo pongo ya que en el caso de que se encuentre una letra minuscula, convierte toda la cadena en mayuscula completa, por lo tanto 
							// no hace falta seguir buscando dentro del event.data si hay mas letras minusculas. 
							break;
						}
					} 
					// lo de añadir el caracter de dos puntos, sólo lo hago para el caso de que haya hasta cuatro de estos, en el 4 lo añado  pero ya tendria 5, por lo 
					// no sigo. 
					// Por otro lado el uso del split, lo que hace es dividir en mas cadenas de texto, la que se haya instanciado, de manera que en el caso de una
					// MAC completa, devuelve 6 cadenas y entre estas 6 hay 5 dos puntos (por ejemplo). Esto lo hago para obtener la cantidad de dos puntos. 
					if ((miMacAddressDelRobot.value.split (':').length -1) < 5){
						if ((miMacAddressDelRobot.value.length == 2) || (miMacAddressDelRobot.value.length == 5) || 
						(miMacAddressDelRobot.value.length == 8) || (miMacAddressDelRobot.value.length == 11) || (miMacAddressDelRobot.value.length == 14)){
							miMacAddressDelRobot.value = miMacAddressDelRobot.value + ":";
						}
					}
				}
			}
			miMacAddressDelRobotAnterior = miMacAddressDelRobot.value;
		}
	);

	let miBotonEnviar = document.getElementById ("botonEnviarId");
	miBotonEnviar.addEventListener ("click", function (event){
			miVerdadMacValidada = true;
			miArrayLugarDondeEstanLosDosPuntos = [2,5,8,11,14];
			miArrayLugarDondeEstanLosCaracteres = [];

			if (miMacAddressDelRobot.value.length < 17){
				alert ("La MAC debe de tener al menos 17 caracteres. ");
				// de esta forma consigo que no se enviaa el formulario.
				event.preventDefault ();
			}else{
				// con este for, lo que hago es recorrer todo el string da la MAC comprobando caracter a caracter si es válido. 
				for (let i = 0; i < 17; i++ ){
					// en este caso examino los caracteres hexagesimal. 
						if (miArrayLugarDondeEstanLosDosPuntos.includes(i) == false){
							if (/[^0-9a-fA-F]/.test(miMacAddressDelRobot.value[i]) ){
							miVerdadMacValidada = false;
							break;
						}
					// en este caso examino las posiciones de los dos puntos. 
					}else{
						if (miMacAddressDelRobot.value[i] != ':'){
							miVerdadMacValidada = false;
							break;
						}
					}
				}
				if (miVerdadMacValidada == false){
					alert ("Debe de introducir una MAC correcta, los caracteres deben ser hexagesimal, y el formato debe ser XX:XX:XX:XX:XX:XX");
					event.preventDefault ();
				}
			}
		}
	);
}


window.addEventListener ("load", validarMac, false);
