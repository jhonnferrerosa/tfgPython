function ejecuta() {
    if (navigator.sendBeacon){
        navigator.sendBeacon('/cierranavegador/', '');
    }else{
        fetch('/cierranavegador/', {
            method: 'POST',
            keepalive: true,
            body: ''
        });
    }

}

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
        ejecuta();
    }
});

window.addEventListener('onbeforeunload', function(event) {
    ejecuta();
});