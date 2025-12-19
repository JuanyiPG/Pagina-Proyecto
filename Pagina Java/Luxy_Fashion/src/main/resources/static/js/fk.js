document.querySelectorAll(".btn-eliminar").forEach(btn => {
    btn.addEventListener("click", () => {

        const id = btn.dataset.id;

        if (!id) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo obtener el ID del empleado'
            });
            return;
        }

        Swal.fire({
            title: '¿Eliminar empleado?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {

            if (!result.isConfirmed) return;

            fetch(`/admin/empleado/eliminar/${id}`)
                .then(async response => {
                    const text = await response.text();
                    if (!response.ok) throw new Error(text);
                    return text;
                })
                .then(msg => {
                    Swal.fire({
                        icon: 'success',
                        title: 'Listo 😎',
                        text: msg
                    }).then(() => {
                        location.reload();
                        // o: btn.closest("tr").remove();
                    });
                })
                .catch(err => {
                    Swal.fire({
                        icon: 'error',
                        title: 'No se pudo eliminar',
                        text: err.message
                    });
                });

        });
    });
});
