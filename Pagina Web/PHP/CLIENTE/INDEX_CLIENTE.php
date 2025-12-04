<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_CLIENTE.php";  

$datos = [];
$obj = new CLIENTE();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_CLIENTE($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gestion CLientes</title>
   <link rel="stylesheet" href="../../CSS/index.css">
  </head>
<body class="body2">

  <div class="main">
    <div class="card">
      <h1>Gestión Clientes</h1>

     
      <form action="INSERTAR_CLIENTE.php" method="post">
        <div class="form-group">
          <input type="text" name="id_cliente" placeholder="Código" required>
          <input type="text" name="nom_cliente" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="direccion_cliente" placeholder="Direccion"required>
        </div>
        <div class="form-group">
          <input type="text" name="telefono_cliente" placeholder="telefono"required>
          <input type="text" name="correo_cliente" placeholder="Correo"required>
        </div>
        <div class="form-group">
          <input type="text" name="nombre_usuari" placeholder="Nombre de usuario"required>
          <input type="text" name="contra" placeholder="Contraseña"required>
        </div>
        <div class="form-group">
          <input type="text" name="id_rol_fk_cliente" placeholder="Numero de rol"required>
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
          <th>Telefono</th>
          <th>Correo</th>
          <th>nombre de usuario</th>
          <th>contraseña</th>
          <th>Numero de rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_cliente']; ?></td>
            <td><?php echo $row['nom_cliente']; ?></td>
            <td><?php echo $row['direccion_cliente']; ?></td>
            <td><?php echo $row['telefono_cliente']; ?></td>
            <td><?php echo $row['correo_cliente']; ?></td>
            <td><?php echo $row['nombre_usuari']; ?></td>
            <td><?php echo $row['contra']; ?></td>
            <td><?php echo $row['id_rol_fk_cliente']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_CLIENTE.php?id_cliente=<?php echo $row['id_cliente']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_CLIENTE.php?id_cliente=<?php echo $row['id_cliente']; ?>"
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
<!-----JAVA SCRIPT--------->

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
