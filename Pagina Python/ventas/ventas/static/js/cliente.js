// ---------------- descripción expandible ----------------
document.addEventListener("DOMContentLoaded", () => {
    const headerDesc = document.querySelector('.descripcion-header');
    const textoDesc = document.getElementById('descrip_produc');
    const arrowDesc = document.querySelector('.arrow-desc');

    if (headerDesc && textoDesc && arrowDesc) {
    headerDesc.addEventListener('click', () => {
        textoDesc.classList.toggle('show');
        textoDesc.classList.toggle('hidden');
        arrowDesc.classList.toggle('rotate');
    });
    }
});