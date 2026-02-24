document.querySelectorAll(".btn-eliminar").forEach(btn => {
    btn.addEventListener("click", () => {

        const id = btn.dataset.id;
        if (!confirm("¿Seguro que deseas eliminar?")) return;

        fetch(`/admin/facturacompra/eliminar/${id}`)
            .then(res => res.text())
            .then(msg => alert(msg));
    });
});
