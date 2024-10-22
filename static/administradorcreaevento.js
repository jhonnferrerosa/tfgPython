/**
 * @function validarFechas
 * @description  esta funcion lo que hace es que no permite que se pueda elegir una fecha anterior a dos horas antes desde el navegador, de esta forma consigo que no se pueda marcar  
 * una fecha pasada en el tiempo, y que se pueda poner un robot en un evento en una facha que ya ha pasado. 
 */
function validarFechas() {
	//alert ("validarFechas()---");
	//console.log ("validarFechas()----");

    const ahora = new Date().toISOString().slice(0, 10); // extrae la fecha actual, cogiendo 16 valores de la fecha global, es decir la que lleva segundos y milesimas. 
	document.querySelectorAll('input[type="date"]').forEach(input => {input.min = ahora});



	//console.log ("validarFechas()----ahora: ", ahora);
	//console.log ("validarFechas()----", new Date().toISOString());	
}


/**
 * @function usarDatePickerComienzo
 * @description  esta funcion lo que hace es establecer el estilo de calendario a todos los elementos en los que quiero usar el datepicker
 */
function usarDatePickerComienzo (){
	// en esta losta voy a guardar todos los elementos HTML en los que tenga que establacer el datepicker que quiero. 
	let miListaCamposAestablecerCalendario = [];
	// con esto tengo todos los div del HTML. 
	let miListaTodosLosDIV = document.getElementsByTagName('div'); 
	// con este fot lo que hago es buscar en cada uno de esos DIV, cuales son los que tiene un id que empieze por fechaComienzoEnEvento_
	const ahora = new Date().toISOString().slice(0, 10);
	for (let i = 0; i < miListaTodosLosDIV.length; i++) {
		if (miListaTodosLosDIV[i].id.startsWith('fechaComienzoEnEvento_')) {
			miListaCamposAestablecerCalendario.push (miListaTodosLosDIV[i].id);
		}
	}
	
	// en este for lo que hago es aplicar a cada uno de los ID el estilo del calendarrio. 
	for (let i = 0; i < miListaCamposAestablecerCalendario.length; i++){
		$(function () {
			$("#" + miListaCamposAestablecerCalendario[i]).datetimepicker({
				icons: { time: 'far fa-clock' },
				format : 'YYYY-MM-DD HH:mm',
				minDate: ahora
			});
		});
	}
}


/**
 * @function usarDatePickerFin
 * @description  esta funcion lo que hace es establecer el estilo de calendario a todos los elementos en los que quiero usar el datepicker
 */
function usarDatePickerFin (){
	let miListaCamposAestablecerCalendario = [];
	let miListaTodosLosDIV = document.getElementsByTagName('div'); 
	const ahora = new Date().toISOString().slice(0, 10);

	for (let i = 0; i < miListaTodosLosDIV.length; i++) {
		if (miListaTodosLosDIV[i].id.startsWith('fechaFinEnEvento_')) {
			miListaCamposAestablecerCalendario.push (miListaTodosLosDIV[i].id);
		}
	}
	for (let i = 0; i < miListaCamposAestablecerCalendario.length; i++){
		$(function () {
			$("#" + miListaCamposAestablecerCalendario[i]).datetimepicker({
				icons: { time: 'far fa-clock' }, 
				format : 'YYYY-MM-DD HH:mm',
				minDate: ahora
			});
		});
	}
}







window.addEventListener ("load", validarFechas, false);
window.addEventListener ("load", usarDatePickerComienzo, false);
window.addEventListener ("load", usarDatePickerFin, false);