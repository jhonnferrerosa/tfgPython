function ejecuta() {

    fetch('/cierranavegador/', {
        method: 'POST',
        keepalive: true,
        body: ''
    });
}

var seHizoClicEnUnEnlace = false;

window.addEventListener('click', function(event) {
    if (event.target.tagName === 'A') {
        seHizoClicEnUnEnlace = true;
    }
});

window.addEventListener('beforeunload', function(event) {
    console.log ("beforeunload()--- se hizo clic: ", seHizoClicEnUnEnlace);
    
    if (!seHizoClicEnUnEnlace) {
        ejecuta();
    } else {
        // Resetea la variable para el próximo evento de navegación
        seHizoClicEnUnEnlace = false;
    }
});