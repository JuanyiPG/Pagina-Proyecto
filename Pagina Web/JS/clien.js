(async function () {
  async function loadHeader() {
    try {
      const res = await fetch('../Items/header-indexcliente.php');
      if (!res.ok) throw new Error('No se pudo cargar header: ' + res.status);
      const html = await res.text();
      const container = document.getElementById('header-cliente');
      if (container) container.innerHTML = html;
      return true;
    } catch (err) {
      console.warn('loadHeader falló:', err);
      return false;
    }
  }

  // ------------- inicializadores del header -------------
  function initHeaderInteractions() {
    const btnHamb = document.getElementById('btnHamburguesa');
    const hambMenu = document.getElementById('hamburgerMenu');
    const mainNav = document.getElementById('mainNav');

    if (btnHamb && hambMenu) {
      btnHamb.addEventListener('click', (ev) => {
        ev.stopPropagation();
        hambMenu.classList.toggle('hidden');
        hambMenu.setAttribute('aria-hidden', hambMenu.classList.contains('hidden') ? 'true' : 'false');
      });

      document.addEventListener('click', (e) => {
        if (!hambMenu.contains(e.target) && e.target !== btnHamb) {
          if (!hambMenu.classList.contains('hidden')) hambMenu.classList.add('hidden');
        }
      });
    }

    if (mainNav) {
      const onScroll = () => {
        if (window.scrollY > 650) mainNav.classList.add('scrolled');
        else mainNav.classList.remove('scrolled');
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    const btnUsuario = document.getElementById('btnUsuario');
    const menuUsuario = document.getElementById('menuUsuario');
    const btnCerrar = document.getElementById('btnCerrarSesion');

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

        try { localStorage.removeItem('userToken'); } catch (e) {}
        window.location.href = '../../index.html';
      });
    }
  }

  // ------------- inicializador del slider -------------
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


  const headerLoaded = await loadHeader();
  if (headerLoaded) {
    initHeaderInteractions();
  } else {
    console.warn('Header no cargado: algunos controles del header no funcionarán.');
  }

  initSlider();

})();
