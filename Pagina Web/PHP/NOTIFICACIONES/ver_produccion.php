<?php
header("Content-Type: text/html; charset=UTF-8");

$file = __DIR__ . "/produccion.json";
$pedidos = [];

if (file_exists($file)) {
    $json = file_get_contents($file);
    $pedidos = json_decode($json, true) ?? [];
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Producción</title>
    <style>
        * {
        margin: 0;
        padding: 0; 
        box-sizing: border-box;
        }
        body {
        display: flex;
        height: 100vh;
        background-color: #f5f6fa;
        }

      .card {
      background: #ffffff;
      padding: 40px;
      border-radius: 15px;
      max-width: 1900px;
      margin: 10px 10px 10px 60px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

        h2 {
            text-align: center;
            margin-bottom: 20px;
            color: #5c0a2e; /* burdeos */
        }

 table {
      width: 100%;
      border-collapse: collapse;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    table th, table td {
      padding: 12px;
      text-align: center;
      border-bottom: 1px solid #ddd;
    }

    table th {
      background: #5e0925;
      color: white;
      font-size: 14px;
    }

    table td {
      font-size: 14px;
    }

        tr:nth-child(even) {
            background-color: #f8f8f8;
        }
        th {
            font-weight: bold;
        }

/*----Header------*/

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

li a {
      text-decoration: none; 
      color: inherit;
      display: block;
    }

    .filtro {
      display: none; 
    }
    </style>
</head>
<body>
      <aside class="sidebar">
    <ul class="list_sidebar">
      <li class="element_sidebar">

            <img src="../../IMG/logoB.png" class="sidebar_icon_logo" style="height: 55px; width:40px;">

            <div class="sidebar_hide">
                <img src="../../IMG/Luxy LL.png" class="sidebar-logo"style="width: 150px; height: 50px;"> 
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
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house" viewBox="0 0 16 16">
            <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5z"/>
        </svg>
        <div class="sidebar_hide">
        <a href="../index-admin.php">
        <p class="sidebar_text">Inicio</p>
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
        <li><a href="../ROL/INDEX_ROL.php" class="sidebar_hide_a">Rol</a></li>
        <li><a href="../CLIENTE/INDEX_CLIENTE.php" class="sidebar_hide_a">Cliente</a></li>
        <li><a href="../EMPLEADO/INDEX_EMPLEADO.php" class="sidebar_hide_a">Empleado</a></li>
        <li><a href="../FACTURA_COMPRA/INDEX_FACTURAC.php" class="sidebar_hide_a">Factura Compra</a></li>
        <li><a href="../FACTURA_VENTA/INDEX_FACTURAV.php" class="sidebar_hide_a">Factura Venta</a></li>
        <li><a href="../MATERIA_PRIMA/INDEX_MATERIAP.php" class="sidebar_hide_a">Materia Prima</a></li>
        <li><a href="../PEDIDO/INDEX_PEDIDO.php" class="sidebar_hide_a">Pedidos</a></li>
        <li><a href="../PRODUCCION/INDEX_PRODUCCION.php" class="sidebar_hide_a">Producción</a></li>
        <li><a href="../PRODUCTO_TERMINADO/INDEX_PRODUCTOT.php" class="sidebar_hide_a">Productos Terminados</a></li>
      </ul>

    </ul>
      <a href="../../index.html"class="element_sidebar sidebar_element_avatar link-m-l">
            <svg class="sidebar_icon sidebar_icon_avatar" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-box-arrow-left" viewBox="0 0 16 16">
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
    <div class="card">
        <h2>PEDIDOS PARA PRODUCCION</h2>
        <?php if (empty($pedidos)): ?>
            <p style="text-align:center;">No hay pedidos enviados todavía.</p>
        <?php else: ?>
          <input type="search" class="buscador form-control mb-3" id="buscador" name="buscador">
        <table>
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Talla</th>
                    <th>Color</th>
                    <th>Categoría</th>
                    <th>Material</th>
                    <th>Cantidad</th>
                    <th>Descripción</th>
                    <th>Fecha</th>
                    <th>Subtotal</th>
                    <th>Valor</th>
                    <th>Estado</th>
                    <th>Cliente</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($pedidos as $p): ?>
                    <tr>
                        <td class='articulos'><?= $p['id_pedido'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['nombre'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['talla'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['color'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['categoria'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['material'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['cantidad'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['descripcion'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['fecha'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['subtotal'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['valor'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['estado'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['cliente'] ?? '-' ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>
    </div>
    <script>
      document.addEventListener('keyup', e =>{
        if (e.target.matches('#buscador')){
          document.querySelectorAll('.articulos').forEach(fruta => {
            fruta.textContent.toLowerCase().includes(e.target.value) 
            ? fruta.classList.remove('filtro')
            : fruta.classList.add('filtro')

          })
        }
      })
      </script>
</body>
</html>
