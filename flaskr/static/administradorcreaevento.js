
// esto vala para que en el caso de que elija uno de los lugares por defecto que están en la BBDD,
// lo que haga sea que algunos campos queden inutilizados y que no se pueda escribir en ellos. 
    
function  miFuncionHabilitarCampos () {
    var calleDelEventoInput = document.getElementById('calleDelEvento');
    var numeroDelEventoInput = document.getElementById('numeroDelEvento');
    var codigoPostalInput = document.getElementById('codigoPostal');
    var edificioDondeSeCelebraInput = document.getElementById('edificioDondeSeCelebra');
    if (this.value !== '-1') {
        console.log ("ahora no se puede editar. ");
        calleDelEventoInput.value = "";
        numeroDelEventoInput.value = "";
        codigoPostalInput.value = null;
        edificioDondeSeCelebraInput.value = "";

        calleDelEventoInput.disabled = true;
        numeroDelEventoInput.disabled = true;
        codigoPostalInput.disabled = true;
        edificioDondeSeCelebraInput.disabled = true;
        } else {
        console.log ("SI se puede editar. ");
        calleDelEventoInput.disabled = false;
        numeroDelEventoInput.disabled = false;
        codigoPostalInput.disabled = false;
        edificioDondeSeCelebraInput.disabled = false;
    }
};

// el evento es que se hayan cargado todas las etiquetas, es decir todos los elementos 
// del DOM. Document Object Model. 
window.addEventListener("DOMContentLoaded", function (){  
    var posiblesEventosAntiguos = document.getElementById('posiblesEventosAntiguos');
    posiblesEventosAntiguos.addEventListener ('change', miFuncionHabilitarCampos, false);
});
