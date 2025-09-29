<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_MATERIAP.php";  

$datos = [];
$obj = new MATERIA_P();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_MATERIA_P($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Materia prima</title>
  <link rel="stylesheet" href="../../CSS/index.css">
</head>
<body class="body2">


  <div class="main">
    <div class="card">
      <h1>Gestión de Materia prima</h1>

     
      <form action="INSERTAR_MATERIAP.php" method="post">
        <div class="form-group">
          <input type="text" name="id_materia_p" placeholder="Código" required>
          <input type="text" name="nom_materia_p" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="color_materia_p" placeholder="Color">
             <input type="text" name="categoria_mp" placeholder="Categoria">
        </div>
        <div class="form-group">
          <input type="text" name="tipo_material_materia_p" placeholder="Tipo de material">
        </div>
        <div class="form-group">
          <input type="text" name="stock_actual_materia_p" placeholder="Stock actual">
          <input type="text" name="stock_minimo_materia_p" placeholder="Stock minimo">
        </div>
        <div class="form-group">
          <input type="text" name="descripcion_materia_p" placeholder="Descripcion">
        </div>
        <div class="form-group">
          <input type="text" name="estado_materia_p" placeholder="Estado">
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
          <th>Color</th>
          <th>Categoria</th>
          <th>Tipo de material</th>
          <th>Stock actual</th>
          <th>Stock minimo</th>
          <th>descripcion</th>
          <th>estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_materia_p']; ?></td>
            <td><?php echo $row['nom_materia_p']; ?></td>
            <td><?php echo $row['color_materia_p']; ?></td>
            <td><?php echo $row['categoria_mp']; ?></td>
            <td><?php echo $row['tipo_material_materia_p']; ?></td>
            <td><?php echo $row['stock_actual_materia_p']; ?></td>
            <td><?php echo $row['stock_minimo_materia_p']; ?></td>
            <td><?php echo $row['descripcion_materia_p']; ?></td>
            <td><?php echo $row['estado_materia_p']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_MATERIAP.php?id_materia_p=<?php echo $row['id_materia_p']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_MATERIAP.php?id_materia_p=<?php echo $row['id_materia_p']; ?>"
              onclick="return confirm('¿Deseas eliminar este rol?');">Eliminar</a>
            </td>
          </tr>
        <?php } ?>
        <?php } else {?>
        <tr><td colspan="5">No se encontraron resultados</td></tr>
<?php } ?>
      </tbody>
    </table>
  </div>
<!-----------JAVA SCRIPT ------------->
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
