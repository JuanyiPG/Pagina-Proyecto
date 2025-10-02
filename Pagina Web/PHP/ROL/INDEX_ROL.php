<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_ROL.php";  

$datos = [];
$obj = new ROL();
    
$search= (isset($_GET['search']))? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_ROL($search); 
?>



<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Roles</title>
  <link rel="stylesheet" href="../../CSS/index.css">
  <style>
    .alerta {
  margin: 15px 0;
  padding: 10px;
  border-radius: 8px;
  font-size: 15px;
}
.alerta p {
  margin: 0;
}
  </style>
  <body class="body2">

  <div class="main">
    <div class="card">
      <h1>Gestión de roles</h1>


      <form action="INSERTAR_ROL.php" method="post">
        <div class="form-group">
          <input type="text" name="id_rol" placeholder="Código" required>
          <input type="text" name="nombre_rol" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="descripcion" placeholder="Descripcion">
        </div>
        <div class="form-group">
          <input type="text" name="estado" placeholder="Estado">
        </div>
        <button type="submit" class="save-btn" onclick="" return>Insertar</button>
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
          <th>Descripcion</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_rol']; ?></td>
            <td><?php echo $row['nombre_rol']; ?></td>
            <td><?php echo $row['descripcion']; ?></td>
            <td><?php echo $row['estado']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_ROL.php?id_rol=<?php echo $row['id_rol']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_ROL.php?id_rol=<?php echo $row['id_rol']; ?>"
              onclick="return confirm('¿Deseas eliminar este rol?')";>Eliminar</a>
            </td>
          </tr>
        <?php } ?>
        <?php } else { ?>
    <tr><td colspan="5">No se encontraron resultados</td></tr>
<?php } ?>
      </tbody>
    </table>
<!------JAVA SCRIPT-------->
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
