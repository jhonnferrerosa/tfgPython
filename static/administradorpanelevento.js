/**
 * @function permitirborrado
 * @description  esta funcion lo que hace es que mosstrar al cliente un aviso de si esta seguro que desea borrar el evento. 
*/
function permitirborrado() {
    //console.log ("permitirborrado()---");
    let misBotonesBorrar = document.querySelectorAll('[id^="botonborrarevento"]');

    for (let i = 0; i < misBotonesBorrar.length; i++){
        //console.log ("permitirborrado()---",  i);
        misBotonesBorrar[i].addEventListener ('click', function(event){
            let miMensajeConfirmacion = confirm ("Esta seguro que desea borrar el evento?");
            if (miMensajeConfirmacion == false){
                event.preventDefault();
            }
        });
    }
}







window.addEventListener ("load", permitirborrado, false);