

/**
 * @function comenzar
 * @description  esta funcion lo que hace es que mostar u ocultar la contraseña en el navegador cliente. 
*/
function comenzar() {
	//alert ("comenzar()---");
	//console.log ("comenzar()----");   
    miCheckbox = document.getElementById("opcionMostrarContrasena");
    miContrasena = document.getElementById ("contrasena");
    miConfirmarContrasena = document.getElementById ("confirmarContrasena");
    miCheckbox.addEventListener('change', function (){
            //console.log(miCheckbox.checked);

            if (miCheckbox.checked){
                miContrasena.type = "text";
                miConfirmarContrasena.type = "text";
                //console.log ("comenzar()---- es true.");
            }else{
                miContrasena.type = "password";
                miConfirmarContrasena.type = "password";
                //console.log ("comenzar()---- es false.");
            }
        }
    );

    let miBotonSignup = document.getElementById ("botonSignup");
    miBotonSignup.addEventListener ("click", function (event){
        if (miContrasena.value != miConfirmarContrasena.value){
            alert ("Las contrseñas deben de coincidir. ");
            event.preventDefault ();
        }
    });

}
window.addEventListener ("load", comenzar, false);

