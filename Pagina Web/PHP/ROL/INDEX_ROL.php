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
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
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
          <input type="text" name="nom_rol" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="desc_rol" placeholder="Descripcion">
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
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_rol']; ?></td>
            <td><?php echo $row['nom_rol']; ?></td>
            <td><?php echo $row['desc_rol']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_ROL.php?id_rol=<?php echo $row['id_rol']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_ROL.php?id_rol=<?php echo $row['id_rol']; ?>"
              onclick="confirmarEliminacion(event, this)";>Eliminar</a>
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

function confirmarEliminacion(e, enlace) {
  e.preventDefault(); // evita que se ejecute de inmediato
  Swal.fire({
    title: '¿Eliminar rol?',
    text: "Esta acción no se puede deshacer.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e74c3c',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = enlace.href;
    }
  })
}


  </script>

</body>
</html>
