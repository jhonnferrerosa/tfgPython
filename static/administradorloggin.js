


function comenzar() {
	//alert ("comenzar()---");
	//console.log ("comenzar()----");
    
    miCheckbox = document.getElementById("opcionMostrarContrasena");
    miContrasena = document.getElementById ("contrasena");
    miCheckbox.addEventListener('change', function (){
            //console.log(miCheckbox.checked);

            if (miCheckbox.checked){
                miContrasena.type = "text";
                //console.log ("comenzar()---- es true.");
            }else{
                miContrasena.type = "password";
                //console.log ("comenzar()---- es false.");
            }
        }
    );

}

window.addEventListener ("load", comenzar, false);

