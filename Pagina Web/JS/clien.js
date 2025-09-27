
document.addEventListener('DOMContentLoaded', () => {
  try {
    const slider = document.querySelector('.slider');
    const leftBtn = document.querySelector('.arrow.left');
    const rightBtn = document.querySelector('.arrow.right');

    if (slider && leftBtn && rightBtn) {
      // duplicar contenido solo si hay items
      if (slider.children.length > 0) {
        slider.innerHTML += slider.innerHTML;
      }

      // calcular scrollStep dinámicamente si hay .item, si no usar 250
      const firstItem = slider.querySelector('.item');
      const computed = firstItem ? getComputedStyle(firstItem) : null;
      const gap = computed ? (parseFloat(computed.marginLeft) + parseFloat(computed.marginRight)) : 0;
      const scrollStep = firstItem ? firstItem.offsetWidth + gap : 250;
      let scrollAmount = 0;
      const totalWidth = slider.scrollWidth / 2; // ancho del bloque original

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

  // ---------- BOTÓN AGREGAR AL CARRITO----------
  try {
    const addcarshop = document.getElementById('add-car-shop');
    if (addcarshop) {
      addcarshop.addEventListener('click', function () {

        alert('Producto agregado al carrito');
      });
    } else {
      console.warn('No se encontró el botón #add-car-shop');
    }
  } catch (err) {
    console.error('Error al inicializar add-car-shop:', err);
  }
});


