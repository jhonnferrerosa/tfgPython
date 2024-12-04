


/**
 * @function validarURL
 * @description  esta funcion lo que hace es que sólo permite caracteres alfanumñericos dentro del campo URL,  a la hora de crear un evento. 
 */
function validarURL() {
    let miURLescritaAnterior = null;
    let miURL = document.getElementById ("codigoQR");
    miURL.addEventListener ("input", function (event){
        if (event.data != null){
            if (/^[a-zA-Z0-9]+$/.test(event.data) == false){
                alert ("En la URL sólo se permite caracteres alfanuméricos");
                miURL.value = miURLescritaAnterior;
            }
        }
        miURLescritaAnterior = miURL.value;
    });
}





window.addEventListener ("load", validarURL, false);

