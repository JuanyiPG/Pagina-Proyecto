document.addEventListener("DOMContentLoaded", function() {
    const mensaje = document.getElementById("mensaje");
    if (mensaje) {
        // Mostrar el mensaje (opcional, en caso que venga oculto)
        mensaje.style.display = "block";
        setTimeout(() => {
            mensaje.style.display = "none";
        }, 3000);
    }
});
