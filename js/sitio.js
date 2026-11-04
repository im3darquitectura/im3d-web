/* IM3D Arquitectura — menú móvil, lightbox de galerías y mensaje del formulario */
(function () {
  // Menú móvil
  var btn = document.querySelector('.menu-btn');
  var menu = document.querySelector('.menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierto');
      btn.setAttribute('aria-expanded', abierto ? 'true' : 'false');
      document.body.style.overflow = abierto ? 'hidden' : '';
    });
  }

  // Lightbox
  var fotos = Array.prototype.slice.call(document.querySelectorAll('.galeria .foto'));
  var lb = document.getElementById('lightbox');
  if (fotos.length && lb) {
    var lbImg = lb.querySelector('img');
    var actual = 0;
    function mostrar(i) {
      actual = (i + fotos.length) % fotos.length;
      lbImg.src = fotos[actual].getAttribute('href');
      lbImg.alt = fotos[actual].querySelector('img').alt;
      lb.hidden = false;
      document.body.style.overflow = 'hidden';
    }
    function cerrar() {
      lb.hidden = true;
      document.body.style.overflow = '';
    }
    fotos.forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); mostrar(i); });
    });
    lb.querySelector('.lb-cerrar').addEventListener('click', cerrar);
    lb.querySelector('.lb-prev').addEventListener('click', function () { mostrar(actual - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { mostrar(actual + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) cerrar(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') cerrar();
      if (e.key === 'ArrowLeft') mostrar(actual - 1);
      if (e.key === 'ArrowRight') mostrar(actual + 1);
    });
    // deslizar en móvil
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) mostrar(actual + (dx < 0 ? 1 : -1));
    });
  }

  // Confirmación del formulario (?enviado=1)
  if (/[?&]enviado=1/.test(location.search)) {
    var ok = document.querySelector('.form-ok');
    if (ok) { ok.hidden = false; ok.scrollIntoView({ block: 'center' }); }
  }
})();
