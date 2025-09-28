// clien.js (reemplaza el contenido anterior)
document.addEventListener('DOMContentLoaded', () => {
  /* -------------------- CARRUSEL (seguro) -------------------- */
  try {
    const slider = document.querySelector('.slider');
    const leftBtn = document.querySelector('.arrow.left');
    const rightBtn = document.querySelector('.arrow.right');

    if (slider && leftBtn && rightBtn) {
      if (slider.children.length > 0) slider.innerHTML += slider.innerHTML;

      const firstItem = slider.querySelector('.item');
      const computed = firstItem ? getComputedStyle(firstItem) : null;
      const gap = computed ? (parseFloat(computed.marginLeft) + parseFloat(computed.marginRight)) : 0;
      const scrollStep = firstItem ? firstItem.offsetWidth + gap : 250;
      let scrollAmount = 0;
      const totalWidth = slider.scrollWidth / 2;

      const doNext = () => {
        scrollAmount += scrollStep;
        if (scrollAmount >= totalWidth) {
          scrollAmount = 0;
          slider.style.transition = "none";
          slider.style.transform = `translateX(-${scrollAmount}px)`;
          void slider.offsetWidth;
          slider.style.transition = "transform 0.5s ease-in-out";
        }
        slider.style.transform = `translateX(-${scrollAmount}px)`;
      };

      const doPrev = () => {
        scrollAmount -= scrollStep;
        if (scrollAmount < 0) {
          scrollAmount = Math.max(totalWidth - scrollStep, 0);
          slider.style.transition = "none";
          slider.style.transform = `translateX(-${scrollAmount}px)`;
          void slider.offsetWidth;
          slider.style.transition = "transform 0.5s ease-in-out";
        }
        slider.style.transform = `translateX(-${scrollAmount}px)`;
      };

      rightBtn.addEventListener('click', doNext);
      leftBtn.addEventListener('click', doPrev);

      let auto = setInterval(doNext, 4000);
      slider.addEventListener('mouseenter', () => clearInterval(auto));
      slider.addEventListener('mouseleave', () => auto = setInterval(doNext, 4000));
    }
  } catch (err) {
    console.error('Error en la lógica del carrusel:', err);
  }

  /* -------------------- CARGAR HEADER (si existe) -------------------- */
  (async () => {
    try {
      const res = await fetch('../Items/header-productocliente.html');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.text();
      const headerCliente = document.getElementById('header-productocliente');
      if (headerCliente) headerCliente.innerHTML = data;
    } catch (err) {
      console.warn('No se pudo cargar header-productocliente (quizá no existe):', err);
    }
  })();

  /* -------------------- DESPLEGABLE "DESCRIPCIÓN" (seguro) -------------------- */
  try {
    const descripcionHeaders = document.querySelectorAll('.descripcion-header');

    descripcionHeaders.forEach(header => {
      const container = header.closest('.descripcion-container');
      if (!container) return; 

      const content = container.querySelector('#descrip-produc') || container.querySelector('.descripcion-content');
      const arrow = header.querySelector('.arrow');

      if (!content || !arrow) return; 

      content.classList.add('hidden');
      arrow.classList.remove('rotate');

      header.addEventListener('click', () => {
        const isOpen = !content.classList.contains('show');
        content.classList.toggle('show', isOpen);
        content.classList.toggle('hidden', !isOpen);
        arrow.classList.toggle('rotate', isOpen);
      });
    });
  } catch (err) {
    console.error('Error inicializando desplegables:', err);
  }

  /* -------------------- BOTÓN "COMPRAR" -------------------- */
  try {
    const addcarshop = document.getElementById('add-car-shop');
    if (addcarshop) {
      addcarshop.addEventListener('click', (e) => {
        e.preventDefault();
        const tallaEl = document.querySelector('input[name="talla"]:checked');
        const colorEl = document.querySelector('input[name="color"]:checked');
        const talla = tallaEl ? tallaEl.value : 'No seleccionada';
        const color = colorEl ? colorEl.value : 'No seleccionada';
        alert(`Producto agregado al carrito.\nTalla: ${talla}\nColor: ${color}`);
      });
    }
  } catch (err) {
    console.error('Error al inicializar add-car-shop:', err);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const headerDesc = document.querySelector('.descripcion-header');
  const textoDesc = document.getElementById('descrip-produc');
  const arrowDesc = document.querySelector('.arrow-desc');

  if (headerDesc && textoDesc && arrowDesc) {
    headerDesc.addEventListener('click', () => {
      textoDesc.classList.toggle('show');
      textoDesc.classList.toggle('hidden');
      arrowDesc.classList.toggle('rotate');
    });
  }
});
