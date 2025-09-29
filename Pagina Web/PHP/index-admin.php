<?php
require_once "../Items/header-adminn.php"
?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script rel="stylesheet" src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.min.js"></script>
  <title>Admin Dashboard</title>
  <link rel="stylesheet" href="../CSS/index.css">
    <body class="body-3">
  <div class="main-1">
    <div class="header">
      <h1>Bienvenido al panel de administración</h1>
    </div>

    <div class="cards-1">
      <div class="card-1">
        <h3>Usuarios</h3>
        <p>135 registrados</p>
        
      </div>
      <div class="card-1">
        <h3>Ventas</h3>
        <p>34 este mes</p>
      </div>
      <div class="card-1">
        <h3>Ingresos</h3>
        <p>$4,500</p>
      </div>
    </div>
  </div>
  <script>
document.addEventListener("DOMContentLoaded", function() {
  function actualizarNotificaciones() {
    fetch("../PHP/NOTIFICACIONES/contar_notis.php")
      .then(response => response.text())
      .then(data => {
        const noti = document.getElementById("notiCount");
        noti.textContent = data;

        // Ocultar badge si es 0
        if (parseInt(data) === 0) {
          noti.style.display = "none";
        } else {
          noti.style.display = "inline-block";
        }
      })
      .catch(error => console.error("Error cargando notificaciones:", error));
  }

  // Llamar al cargar la página
  actualizarNotificaciones();

  // Refrescar cada 10 segundos
  setInterval(actualizarNotificaciones, 10000);
});
</script>
<!------header----------->
 <script>
    document.addEventListener("DOMContentLoaded", function() {
      const toggleBtn = document.getElementById("formToggle");
      const submenu = document.getElementById("submenuForm");

      toggleBtn.addEventListener("click", function(e) {
        e.preventDefault();
        submenu.classList.toggle("show");
      });
    });
  </script>

</body>
</html>

</html>