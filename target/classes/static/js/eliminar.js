  document.addEventListener("DOMContentLoaded", function() {

  const botonesEliminar = document.querySelectorAll(".btn-eliminar");

    botonesEliminar.forEach(enlace => {
        enlace.addEventListener("click", function(e) {
            e.preventDefault();

            Swal.fire({
                title: '¿Estás seguro?',
                text: "¡No podrás revertir esto!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirige a la URL de eliminar
                    window.location.href = enlace.href;
                }
            });
        });
    });
});