(async function () { //una funsion auto-ejecutable

  // ---------------- inicializadores del header ----------------
  function initHeaderInteractions() { //maneja todo lo que esta en el header
    const btnHamb = document.getElementById('btnHamburguesa');
    const hambMenu = document.getElementById('hamburgerMenu');
    const mainNav = document.getElementById('mainNav');

    if (btnHamb && hambMenu) {
    //si existe evita el error
      btnHamb.addEventListener('click', (ev) => {
        ev.stopPropagation();
        //evita que al haer click suba al documento
        hambMenu.classList.toggle('hidden');
        hambMenu.setAttribute('aria-hidden', hambMenu.classList.contains('hidden') ? 'true' : 'false');
      });

      document.addEventListener('click', (e) => {
      //cerrar el menu al dar click afuera
        if (!hambMenu.contains(e.target) && e.target !== btnHamb) {
          if (!hambMenu.classList.contains('hidden')) hambMenu.classList.add('hidden');
          //si el click no fuen en el menu ni boton, cierra
        }
      });
    }

    if (mainNav) {
    //cambia al hacer scroll
      const onScroll = () => {
        if (window.scrollY > 650) mainNav.classList.add('scrolled');
        else mainNav.classList.remove('scrolled');
        //agrega una clase para cambiar de estilo
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    const btnUsuario = document.getElementById('btnUsuario');
    const menuUsuario = document.getElementById('menuUsuario');
    const btnCerrar = document.getElementById('btnCerrarSesion');
    const btnEditar = document.getElementById('btnEditar');

    if (btnUsuario && menuUsuario) {
      btnUsuario.addEventListener('click', (ev) => {
        ev.stopPropagation();
        menuUsuario.classList.toggle('hidden');
      });
      document.addEventListener('click', (e) => {
        if (!menuUsuario.contains(e.target) && e.target !== btnUsuario) {
          if (!menuUsuario.classList.contains('hidden')) menuUsuario.classList.add('hidden');
        }
      });
    }
    if (btnCerrar) {
      btnCerrar.addEventListener('click', () => {
        try {
          localStorage.removeItem('userToken');
        } catch (e) {}

        window.location.href = '/';
      });
    }

    if (btnEditar) {
      btnEditar.addEventListener('click', () => {
        window.location.href = '/admin/cliente/editar';
      });
    }
  }

  // ---------------- inicializador del slider ----------------
  function initSlider() {
    try {
      const slider = document.querySelector('.slider');
      const leftBtn = document.querySelector('.arrow.left');
      const rightBtn = document.querySelector('.arrow.right');

      if (!slider || !leftBtn || !rightBtn) return;

      const items = slider.querySelectorAll('.item');
      if (items.length > 0 && !slider.dataset.duplicated) {
        slider.innerHTML += slider.innerHTML;
        slider.dataset.duplicated = 'true';
      }

      const firstItem = slider.querySelector('.item');
      const gap = firstItem ? (parseFloat(getComputedStyle(firstItem).marginLeft) + parseFloat(getComputedStyle(firstItem).marginRight)) : 0;
      const scrollStep = firstItem ? firstItem.offsetWidth + gap : 250;
      let scrollAmount = 0;
      const totalWidth = slider.scrollWidth / 2;

      const doNext = () => {
        scrollAmount += scrollStep;
        if (scrollAmount >= totalWidth) {
          scrollAmount = 0;
          slider.style.transition = 'none';
          slider.style.transform = `translateX(-${scrollAmount}px)`;
          void slider.offsetWidth;
          slider.style.transition = 'transform 0.5s ease-in-out';
        }
        slider.style.transform = `translateX(-${scrollAmount}px)`;
      };

      const doPrev = () => {
        scrollAmount -= scrollStep;
        if (scrollAmount < 0) {
          scrollAmount = Math.max(totalWidth - scrollStep, 0);
          slider.style.transition = 'none';
          slider.style.transform = `translateX(-${scrollAmount}px)`;
          void slider.offsetWidth;
          slider.style.transition = 'transform 0.5s ease-in-out';
        }
        slider.style.transform = `translateX(-${scrollAmount}px)`;
      };

      rightBtn.addEventListener('click', doNext);
      leftBtn.addEventListener('click', doPrev);

      let auto = setInterval(doNext, 4000);
      slider.addEventListener('mouseenter', () => clearInterval(auto));
      slider.addEventListener('mouseleave', () => auto = setInterval(doNext, 4000));
    } catch (err) {
      console.error('slider init error:', err);
    }
  }

 /* const headerLoaded = await loadHeader();
  if (headerLoaded) {
    initHeaderInteractions();
  } else {
    console.warn('Header no cargado: algunos controles del header no funcionarán.');
  }

  initSlider();*/
  initHeaderInteractions();
})();

//traer el header echo con th

// ---------------- Add to cart ----------------
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

// ---------------- descripción expandible ----------------
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

  // ---------------- cambio de colores de imágenes ----------------
  const imgprin = document.getElementById('imgprin');
  const img1 = document.getElementById('img1');
  const img2 = document.getElementById('img2');
  const img3 = document.getElementById('img3');

  if (imgprin && img1 && img2 && img3) {
    const cambiarImagenes = (imagenes) => {
      imgprin.src = imagenes[0];
      img1.src = imagenes[1];
      img2.src = imagenes[2];
      img3.src = imagenes[3];
    };

    const botonrojo = document.getElementById('color-rojo');
    if (botonrojo) {
      const imagenroja = [
        '../IMG/blusa-hombro-rojo.jpg',
        '../IMG/blusa-hombro-rojo.jpg',
        '../IMG/blusa-hombro-rojo.jpg',
        '../IMG/blusa-hombro-rojo.jpg',
      ];
      botonrojo.addEventListener('click', () => cambiarImagenes(imagenroja));
    }

    const botonblanco = document.getElementById('color-blanco');
    if (botonblanco) {
      const imagenblanca = [
        '../IMG/blusa-hombro-blanco.jpg',
        '../IMG/blusa-hombro-blanco.jpg',
        '../IMG/blusa-hombro-blanco.jpg',
        '../IMG/blusa-hombro-blanco.jpg',
      ];
      botonblanco.addEventListener('click', () => cambiarImagenes(imagenblanca));
    }

    const botongris = document.getElementById('color-gris');
    if (botongris) {
      const imagengriss = [
        '../IMG/blusa-hombro-gris.jpg',
        '../IMG/blusa-hombro-gris.jpg',
        '../IMG/blusa-hombro-gris.jpg',
        '../IMG/blusa-hombro-gris.jpg',
      ];
      botongris.addEventListener('click', () => cambiarImagenes(imagengriss));
    }

    const botonnegro = document.getElementById('color-negro');
    if (botonnegro) {
      const imagennegra = [
        '../IMG/blusa-hombro-negro.jpeg',
        '../IMG/blusa-hombro-negro.jpeg',
        '../IMG/blusa-hombro-negro.jpeg',
        '../IMG/blusa-hombro-negro.jpeg',
      ];
      botonnegro.addEventListener('click', () => cambiarImagenes(imagennegra));
    }
  }
});
