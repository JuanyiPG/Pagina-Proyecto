<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="../CSS/index.css">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  <title>Empleado dashboard</title>
  <style>
    body{
      display: flex;
      min-height: 100vh;
    }
    /* Main content */
    .main {
      position: relative;
      flex: 1;
      padding: 20px;
    }

    .header {
      background-color: #fff;
      padding: 10px 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .cards {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }

    .card {
      background-color: white;
      padding: 20px;
      border-radius: 8px;
      flex: 1;
      min-width: 200px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .card h3 {
      margin-bottom: 10px;
    }
    .sidebar {
      background-image: linear-gradient(to bottom, rgb(255, 255, 255), #5c0b26);
      width: max-content;
      height: 100vh;
      border: #50061f solid 1px;
      border-radius: 10px;
      padding: 2rem 1rem;
      overflow: scroll;
      display: flex;
      flex-direction: column;
    }

    .list_sidebar_a{
      list-style: none;
      padding: 0;
      margin: 0;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: .4rem;
    }

    .element_sidebar {
      padding: .8rem 1.3rem;
      border-radius: 3px;
      display: grid;
      align-items: center;
      grid-template-columns: 50px 0fr;
      color: #50061f;
      fill: #5c0b26;
      transition: grid-template-columns .4s;
    }

    .sidebar:hover .element_sidebar {
      grid-template-columns: 40px 1fr;
    }

    .element_sidebar:not(:has(.sidebar_icon_logo)):hover {
      background-color: #5e092593;
      color: #fff;
      fill: #fff;
      cursor: pointer;
    }

    .element_sidebar:has(.sidebar_icon_logo) {
      margin-bottom: 1rem;
    }

    .sidebar-icon {
      width: 100%;
      overflow: hidden;
      justify-self: center;
    }

    .sidebar_icon_logo {
      max-width: 50px;
    }

    .sidebar_icon_avatar {
      width: 40px;
      height: 40px;
      object-fit: cover;
      object-position: center;
    }

    .sidebar_element_avatar {
      margin-top: auto;
      text-wrap: nowrap;
      text-align: left;
      color: #fff;
    }

    .sidebar_Title {
      padding-left: 1.3rem;
    }

    .sidebar-logo,
    .sidebar_text {
      padding-left: 1.3rem;
    }

    .sidebar_hide {
      overflow: hidden;
    }

    .sidebar_hide_a {
      text-decoration: none;
      color: inherit;
    }

    .sidebar_hide_a:hover {
      color: #fff;
    }


  .submenu {
      display: none;
      flex-direction: column;
      padding-left: 2rem;
      margin: 0;
      list-style: none;
      gap: .3rem;
    }

    .submenu.show {
      display: flex;
    }

    .submenu li {
      padding: .5rem .8rem;
      font-size: 14px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 5px;
      transition: background 0.3s, color 0.3s;
      color: #50061f;
    }

    .submenu li:hover {
      background: #5c0b26;
      color: #fff;
      cursor: pointer;
    }

    .submenu li a {
      text-decoration: none;
      color: inherit;
      display: block;
    }

    li a {
      text-decoration: none; 
      color: inherit;
      display: block;
    }
.sidebar::-webkit-scrollbar {
  width: 8px;
}

.sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}

  </style>
</head>
<body>
  <aside class="sidebar">
    <ul class="list_sidebar">
      <li class="element_sidebar">

            <img src="../IMG/logoB.png" class="sidebar_icon_logo" style="height: 55px; width:40px;">

            <div class="sidebar_hide">
                <img src="../IMG/Luxy LL.png" class="sidebar-logo"style="width: 150px; height: 50px;"> 
            </div>

      <li class="element_sidebar">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bell" viewBox="0 0 16 16">
             <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2M8 1.918l-.797.161A4 4 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4 4 0 0 0-3.203-3.92zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5 5 0 0 1 13 6c0 .88.32 4.2 1.22 6"/>
          </svg>
        <div class="sidebar_hide">
          <p class="sidebar_text">Notificaciones</p>
        </div>
      </li>
      
      <li class="element_sidebar">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart" viewBox="0 0 16 16">
            <path d="M4 11H2v3h2zm5-4H7v7h2zm5-5v12h-2V2zm-2-1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM6 7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1zm-5 4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1z"/>
         </svg>
        <div class="sidebar_hide">
          <a href="index-emple.php">
          <p class="sidebar_text">Estadisticas</p>
          </a>
        </div>
      </li>

      <li class="element_sidebar" id="formToggle">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-grid" viewBox="0 0 16 16">
           <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5z"/>
        </svg>
        <div class="sidebar_hide">
          <p class="sidebar_text">Formularios</p>
        </div>
      </li>

      <ul class="submenu" id="submenuForm">
        <li><a href="FACTURAV_EMPLE/INDEX_FACTURA_EMPLE.php" class="sidebar_hide_a">Factura Venta</a></li>
        <li><a href="PEDIDOS_EMPLE/INDEX_PEDIDOS_EMPLE.php" class="sidebar_hide_a">Pedidos</a></li>
        <li><a href="PRODUCTO_TERMINADO/INDEX_PRODUCTOT.php" class="sidebar_hide_a">Productos Terminados</a></li>
      </ul>

    </ul>
      <a href="../../index.html"class="element_sidebar sidebar_element_avatar link-m-l">
            <svg class="sidebar_icon sidebar_icon_avatar" xmlns="http://www.w3.org/2000/svg" width="10" height="20" fill="currentColor" class="bi bi-box-arrow-left" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M6 12.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v2a.5.5 0 0 1-1 0v-2A1.5 1.5 0 0 1 6.5 2h8A1.5 1.5 0 0 1 16 3.5v9a.5.5 0 0 1-1.5 1.5h-8A1.5 1.5 0 0 1 5 12.5v-2a.5.5 0 0 1 1 0z"/>
                    <path fill-rule="evenodd" d="M.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L1.707 7.5H10.5a.5.5 0 0 1 0 1H1.707l2.147 2.146a.5.5 0 0 1-.708.708z"/>
            </svg>
          <div class="sidebar_hide">
              <p class="sidebar_Title">Cerrar Sesión</p>
          </div>
      </a>
     
  </aside>

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

  <header id="header-emple"></header>

    <div class="main">
    <div class="header">
        <h1>¡Hola! Bienvenido al panel de empleado</h1>
    </div>

    <div class="cards">
        <div class="card">
        <h3>Usuarios</h3>
        <p>135 registrados</p>     
        </div>
        <div class="card">
        <h3>Ventas</h3>
        <p>34 este mes</p>
        </div>
        <div class="card">
        <h3>Ingresos</h3>
        <p>$1,700.000</p>
        </div>
 <a href="../PAGINA_EMPLEADO/INDEX_FACTURA_EMPLE.php"></a>
    </div>
    </div>
</body>
</html>


</html>