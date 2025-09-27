<?php 
require_once "../CONFIG.PHP"; 
require_once "CLASE_EMPLEADO.php";  

$datos = [];
$obj = new EMPLEADO();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_EMPLEADO($search); 
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Producto terminado</title>
  <link rel="stylesheet" href="../CSS/form.css">
  

<style>
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
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house" viewBox="0 0 16 16">
            <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5z"/>
        </svg>
        <div class="sidebar_hide">
          <p class="sidebar_text">Inicio</p>
        </div>
      </li>
      <li class="element_sidebar">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart" viewBox="0 0 16 16">
            <path d="M4 11H2v3h2zm5-4H7v7h2zm5-5v12h-2V2zm-2-1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM6 7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1zm-5 4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1z"/>
         </svg>
        <div class="sidebar_hide">
          <p class="sidebar_text">Estadisticas</p>
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


  <div class="main">
    <div class="card">
      <h1>Gestión de Empleados</h1>

     
      <form action="INSERTAR_EMPLEADO.php" method="post">
        <div class="form-group">
          <input type="text" name="id_empleado" placeholder="Código" required>
          <input type="text" name="nom_empleado" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="direccion_empleado" placeholder="Direccion">
          <input type="text" name="tipo_sangre" placeholder="tipo de sangre">
        </div>
        <div class="form-group">
          <input type="text" name="telefono_empleado" placeholder="Telefono">
          <input type="text" name="correo_empleado" placeholder="Correo">
        </div>
        <div class="form-group">
          <input type="date" name="Fecha_ing_empleado" placeholder="Fecha">
          <input type="text" name="salario_empleado" placeholder="Salario">
        </div>
        <div class="form-group">
          <input type="text" name="Estado_empleado" placeholder="Estado">
          <input type="text" name="nom_usuario" placeholder="Nombre de usuario">
        </div>
        <div class="form-group">
            <input type="text" name="contras" placeholder="Contaseña">
            <input type="text" name="id_rol_fk_empleado" placeholder="Identificador de rol">
        </div>
        <button type="submit" class="save-btn">Insertar</button>
      </form>
    </div>

    <div id="search" class="search"> 
        <form action="" method="get">
            <input type="text" name="search" placeholder="Escribe una palabara" id="searchInput">
            <input type="submit" value="Buscar" id="btnSearch">
        </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nombre</th>
          <th>Direccion</th>
          <th>Tipo de sangre</th>
          <th>Telefono</th>
          <th>Correo</th>
          <th>Fecha de ingreso</th>
          <th>Salario</th>
          <th>Estado</th>
          <th>Nombre de usuario</th>
          <th>Contraseña</th>
          <th>Numero de rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_empleado']; ?></td>
            <td><?php echo $row['nom_empleado']; ?></td>
            <td><?php echo $row['direccion_empleado']; ?></td>
            <td><?php echo $row['tipo_sangre']; ?></td>
            <td><?php echo $row['telefono_empleado']; ?></td>
            <td><?php echo $row['correo_empleado']; ?></td>
            <td><?php echo $row['Fecha_ing_empleado']; ?></td>
            <td><?php echo $row['salario_empleado']; ?></td>
            <td><?php echo $row['Estado_empleado']; ?></td>
            <td><?php echo $row['nom_usuario']; ?></td>
            <td><?php echo $row['contras']; ?></td>
            <td><?php echo $row['id_rol_fk_empleado']; ?></td>
            <td>
              <a class="btn" href="EDITAR_EMPLEADO.php?id_empleado=<?php echo $row['id_empleado']; ?>">Actualizar</a>
              <a class="btn" href="ELIMINAR_EMPLEADO.php?id_empleado=<?php echo $row['id_empleado']; ?>"
              onclick="return confirm('¿Deseas eliminar este rol?');">Eliminar</a>
            </td>
          </tr>
        <?php } ?>
        <?php } else { ?>
    <tr><td colspan="5">No se encontraron resultados</td></tr>
<?php } ?>
      </tbody>
    </table>
  </div>

</body>
</html>
