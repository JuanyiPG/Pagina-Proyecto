<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_PRODUCTO_T.php";  

$datos = [];
$obj = new PRODUCTO_T();
    
$search = (isset($_GET['search'])) ? $_GET['search']: "";
    $datos = $obj->CONSULTAR_PRODUCTO_T($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Producto terminado</title>
  <link rel="stylesheet" href="../../CSS/index.css">
  <body class="body2">


  <div class="main">
    <div class="card">
      <h1>Gestión de productos terminados</h1>

     
      <form action="INSERTAR.php" method="post">
        <div class="form-group">
          <input type="text" name="id_producto_t" placeholder="Código" required>
          <input type="text" name="nombre_producto_t" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="descripcion_producto_t" placeholder="Descripcion">
        </div>
        <div class="form-group">
          <input type="text" name="categoria_produ_t" placeholder="Categoria">
        </div>
        <div class="form-group">
          <input type="text" name="unidad_medida" placeholder="Medida">
          <input type="text" name="estado_producto_t" placeholder="Estado">
        </div>
        <div class="form-group">
          <input type="text" name="id_produccion_fk_producto_terminado" placeholder="Identificador de el el numero de produccion">
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
          <th>Descripcion</th>
          <th>Categoria</th>
          <th>Unidad de medida</th>
          <th>Estado</th>
          <th>Identificador</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          
          <tr>
            <td><?php echo $row['id_producto_t']; ?></td>
            <td><?php echo $row['nombre_producto_t']; ?></td>
            <td><?php echo $row['descripcion_producto_t']; ?></td>
            <td><?php echo $row['categoria_produ_t']; ?></td>
            <td><?php echo $row['unidad_medida']; ?></td>
            <td><?php echo $row['estado_producto_t']; ?></td>
            <td><?php echo $row['id_produccion_fk_producto_terminado']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_PRODUCTOT.php?id_producto_t=<?php echo $row['id_producto_t']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_PRODUCTOT.php?id_producto_t=<?php echo $row['id_producto_t']; ?>"
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
