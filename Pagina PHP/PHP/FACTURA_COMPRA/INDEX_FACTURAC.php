<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_FACTURAC.PHP";  

$datos = [];
$obj = new FACTURA_C();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_FACTURA_C($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fctura compra</title>
  <link rel="stylesheet" href="../../CSS/index.css">
<body class="body2">


  <div class="main">
    <div class="card">
      <h1>Gestión de factura compra</h1>

     
      <form action="INSERTAR_FACRURAC.PHP" method="post">
        <div class="form-group">
          <input type="text" name="cod_factura_compra" placeholder="Código" required>
          <input type="text" name="fecha_factura_compra"= "date" placeholder="Fecha de compra" required
          onfocus="this.type='date'" onblur="if(!this.value) this.type='text'">
        </div>
        <div class="form-group">
          <input type="text" name="total_faactura_compra" placeholder="total de la factura"required>
          <input type="text" name="metododepago_factura_compra" placeholder="Metodo de pago"required>
        </div>
        <div class="form-group">
          <input type="text" name="estado_factura_compra" placeholder="Estado"required>
          <input type="text" name="id_empleado_fk_factura_compra" placeholder="ID empleado que registro la compra"required>
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
          <th>Fecha</th>
          <th>Total</th>
          <th>Metodo de pago</th>
          <th>estado</th>
          <th>Identificador</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['cod_factura_compra']; ?></td>
            <td><?php echo $row['fecha_factura_compra']; ?></td>
            <td><?php echo $row['total_faactura_compra']; ?></td>
            <td><?php echo $row['metododepago_factura_compra']; ?></td>
            <td><?php echo $row['estado_factura_compra']; ?></td>
            <td><?php echo $row['id_empleado_fk_factura_compra']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_FACTURAC.php?cod_factura_compra=<?php echo $row['cod_factura_compra']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_FACTURAC.php?cod_factura_compra=<?php echo $row['cod_factura_compra']; ?>"
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
  <!------JAVA SCRIPT ---------->
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
