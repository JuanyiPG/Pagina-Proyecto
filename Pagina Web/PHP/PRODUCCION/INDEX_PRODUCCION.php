<?php 
require_once "../CONFIG.PHP"; 
require_once "CLASE_PRODUCCION.PHP";  

$datos = [];
$obj = new PRODUCCION();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : ""; 
    $datos = $obj->CONSULTAR_PRODUCCION($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Produccion</title>
  <link rel="stylesheet" href="../../CSS/index.css">
<body class="body2">


  <div class="main">
    <div class="card">
      <h1>Gestión de produccion</h1>

     
      <form action="INSERTAR_PRODUCCION.PHP" method="post">
        <div class="form-group">
          <input type="text" name="id_produccion" placeholder="Numero de produccion" required>
          <input type="text" name="fecha_inicio_produccion" = "text" placeholder="Fecha inicio de produccion " required
          onfocus="this.type='date'" onblur="if(!this.value) this.type='text'">
        </div>
        <div class="form-group">
          <input type="text" name="cantidad_producida" placeholder=" Cantidad"required>
          <input type="text" name="costo_mano_obra" placeholder="Costo de mano de obra"required>
        </div>
        <div class="form-group">
          <input type="text" name="costo_total_materia_prima" id="SubTotal" placeholder="Costo total de la materia prima"required>
          <input type="text" name="costo_iva" id="Iva" placeholder="IVA"required>
        </div>
        <div class="form-group">
          <input type="text" name="costo_total_produccion" id="Total" placeholder="Costo total"required readonly>
          <input type="text" name="fecha_fin_produccion" = "text" placeholder="Fecha fin de produccion" required
                    onfocus="this.type='date'" onblur="if(!this.value) this.type='text'">
        </div>
        <div class="form-group">
          <input type="text" name="estado_produccion" placeholder="estado"required>
          <input type="text" name="id_empleado_fk_produccion" placeholder="numero de el empleado que realizo la produccion"required>
        </div>
        <div class="form-group">
          <input type="text" name="id_pedido_fk_produccion" placeholder="numero de pedido de esta produccion"required>
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
          <th>Fecha de inicio</th>
          <th>Cantidad producida</th>
          <th>Costo mano de obra</th>
          <th>Costo de el material tota utilizado</th>
          <th>IVA</th>
          <th>Total de produccion</th>
          <th>Fecha de finalizacion</th>
          <th>Estado</th>
          <th>numero de empleado que realizo la produccion</th>
          <th>numero de pedido de esta produccion</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_produccion']; ?></td>
            <td><?php echo $row['fecha_inicio_produccion']; ?></td>
            <td><?php echo $row['cantidad_producida']; ?></td>
            <td><?php echo $row['costo_mano_obra']; ?></td>
            <td><?php echo $row['costo_total_materia_prima']; ?></td>
            <td><?php echo $row['costo_iva']; ?></td>
            <td><?php echo $row['costo_total_produccion']; ?></td>
            <td><?php echo $row['fecha_fin_produccion']; ?></td>
            <td><?php echo $row['estado_produccion']; ?></td>
            <td><?php echo $row['id_empleado_fk_produccion']; ?></td>
            <td><?php echo $row['id_pedido_fk_produccion']; ?></td>
            <td>
              <a class="btn" href="EDITAR_PRODUCCION.php?id_produccion=<?php echo $row['id_produccion']; ?>">Actualizar</a>
              <a class="btn" href="ELIMINAR_PRODUCCION.php?id_produccion=<?php echo $row['id_produccion']; ?>"
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
<!-----JAVA SCRIPT----->
<!---------CALCULO------->
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
<!-----HEADER-------->
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
