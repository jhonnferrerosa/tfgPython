
// este Javascript lo que hace es que cuando se cierre la pestaña 

function funcionAvisarEndpoint() {
    fetch('/cierranavegador/', {
        method: 'POST',
        keepalive: true,
        body: ''
    });
}

// esto lo que hace es que si se hace click en un enlace tipo a href que en el caso de que se cierre la 
// pagina, que se comrpueba porque se cerró, de esta manera si fue por un click a href, que no se
// llame al endpoint de cerrar el navegador. 
var seHizoClicEnUnEnlace = false;
window.addEventListener('click', function(event) {
    if (event.target.tagName === 'A') {
        seHizoClicEnUnEnlace = true;
    }
});

function funcionComenzar (){
    console.log ("funcionComenzar()--- se hizo clic: ", seHizoClicEnUnEnlace);

}

// el evento es el momento justo de cerrar la pestaña. 
window.addEventListener('beforeunload', function() {
    //console.log ("beforeunload()--- se hizo clic: ", seHizoClicEnUnEnlace);
    if (seHizoClicEnUnEnlace ==  false) {
        funcionAvisarEndpoint();
    } else {
        // Resetea la variable para el próximo evento de navegación
        seHizoClicEnUnEnlace = false;
    }
});



