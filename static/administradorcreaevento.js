

/**
 * @function validarFechas
 * @description  esta funcion lo que hace es que no permite que se pueda elegir una fecha anterior a dos horas antes desde el navegador, de esta forma consigo que no se pueda marcar  
 * una fecha pasada en el tiempo, y que se pueda poner un robot en un evento en una facha que ya ha pasado. 
 * 
 */
function validarFechas() {
	//alert ("validarFechas()---");
	//console.log ("validarFechas()----");

    const ahora = new Date().toISOString().slice(0, 16); // extrae la fecha actual, cogiendo 16 valores de la fecha global, es decir la que lleva segundos y milesimas. 
	document.querySelectorAll('input[type="datetime-local"]').forEach(input => {input.min = ahora});

	//console.log ("validarFechas()----ahora: ", ahora);
	//console.log ("validarFechas()----", new Date().toISOString());
}

window.addEventListener ("load", validarFechas, false);


