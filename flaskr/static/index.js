function ejecuta() {

    fetch('/cierranavegador/', {
        method: 'POST',
        keepalive: true,
        body: ''
    });
}

window.addEventListener('beforeunload', function(event) {
    ejecuta();
});

