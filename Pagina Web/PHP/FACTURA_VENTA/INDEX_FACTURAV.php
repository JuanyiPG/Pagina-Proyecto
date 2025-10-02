<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_FACTURAV.PHP";  

$datos = [];
$obj = new FACTURA_V();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_FACTURA_V($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fctura Venta</title>
  <link rel="stylesheet" href="../../CSS/index.css">
<body class="body2">

  <div class="main">
    <div class="card">
      <h1>Gestión de factura venta</h1>

     
      <form action="INSERTAR_FACRURAV.PHP" method="post">
        <div class="form-group">
          <input type="text" name="cod_factura_v" placeholder="Código" required>
          <input type="text" name="fecha_factura_v" = "text" placeholder="Fecha" required
          onfocus="this.type='date'" onblur="if(!this.value) this.type='text'">
        </div>
        <div class="form-group">
          <input type="text" name="sub_total_factura_v" id="SubTotal" placeholder=" Sub total de la factura"required>
          <input type="text" name="iva_factura_v" id = "Iva" placeholder="IVA"required>
        </div>
        <div class="form-group">
          <input type="text" name="total_factura_v" id= "Total" placeholder="Total"required readonly >
          <input type="text" name="metodo_pago" placeholder="Metodo de pago"required>
        </div>
        <div class="form-group">
          <input type="text" name="descuento" placeholder="Descuento"required>
          <input type="text" name="estado_factura_venta" placeholder="Estado"required>
        </div>
        <div class="form-group">
          <input type="text" name="id_empleado_fk_factura" placeholder="id_empleado_fk_factura"required>
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
          <th>Numero de empleado que a registro</th>
          <th>Acciones</th>
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
            <td><?php echo $row['id_empleado_fk_factura']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_FACTURAV.php?cod_factura_v=<?php echo $row['cod_factura_v']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_FACTURAV.php?cod_factura_v=<?php echo $row['cod_factura_v']; ?>"
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

<!---------JAVA SCRIPT----->
<!----------CALCULO-------------->
  <script>
    const subTotal = document.getElementById("SubTotal");
    const iva = document.getElementById("Iva");
    const total = document.getElementById("Total");

    function calcularTotal() {
    const sub = parseFloat(subTotal.value) || 0;
    const ivaPct = parseFloat(iva.value) || 0;

    const tot = sub + (sub * ivaPct / 100);

    total.value = tot.toFixed(2); // 2 decimales
    }

    
    subTotal.addEventListener("input", calcularTotal);
    iva.addEventListener("input", calcularTotal);
</script>
<!------HEADER----------------->
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
