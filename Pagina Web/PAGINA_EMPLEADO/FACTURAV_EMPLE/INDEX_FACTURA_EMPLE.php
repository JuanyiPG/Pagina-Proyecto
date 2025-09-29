<?php
require_once "../../Items/header_emple.html"
?>
<?php 
require_once "../FACTURAV_EMPLE/CONEXION.PHP"; 
require_once "../FACTURAV_EMPLE/CLASE_FV.PHP";  


$datos = [];
$obj = new FACTURA_V();
    $search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_FACTURA_V(); 
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fctura Venta</title>
  <link rel="stylesheet" href="../../CSS/index.css">
  <body class="body2">


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
      <h1>Gestión de factura venta</h1>

     
      <form action="../FACTURAV_EMPLE/INSERTAR_FV.PHP" method="post">
        <div class="form-group">
          <input type="text" name="cod_factura_v" placeholder="Código" required>
          <input type="date" name="fecha_factura_v" placeholder="Fecha" required>
        </div>
        <div class="form-group">
          <input type="text" name="sub_total_factura_v" placeholder=" Sub total de la factura"required>
          <input type="text" name="iva_factura_v" placeholder="IVA"required>
        </div>
        <div class="form-group">
          <input type="text" name="total_factura_v" placeholder="Total"required>
          <input type="text" name="metodo_pago" placeholder="Metodo de pago"required>
        </div>
        <div class="form-group">
          <input type="text" name="descuento" placeholder="Descuento"required>
          <input type="text" name="estado_factura_venta" placeholder="Estado"required>
        </div>
        <div>
          <input type="hidden" name="id_empleado_fk_factura" value="2">
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
          <th>Sub total</th>
          <th>IVA</th>
          <th>Total</th>
          <th>metodo de pago</th>
          <th>Descuento</th>
          <th>estado</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['cod_factura_v']; ?></td>
            <td><?php echo $row['fecha_factura_v']; ?></td>
            <td><?php echo $row['sub_total_factura_v']; ?></td>
            <td><?php echo $row['iva_factura_v']; ?></td>
            <td><?php echo $row['total_factura_v']; ?></td>
            <td><?php echo $row['metodo_pago']; ?></td>
            <td><?php echo $row['descuento']; ?></td>
            <td><?php echo $row['estado_factura_venta']; ?></td>

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
