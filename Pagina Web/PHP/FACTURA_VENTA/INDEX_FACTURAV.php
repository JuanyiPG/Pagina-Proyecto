<?php 
require_once "CONEXION.php"; 
require_once "CLASE_FACTURAV.PHP";  

$datos = [];
$obj = new FACTURA_V();
    
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $datos = $obj->ConsultarfacturavtPorID($search); 
} else {
    $datos = $obj->CONSULTAR_FACTURA_V(); 
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fctura Venta</title>
  <link rel="stylesheet" href="../CSS/CSS.css">
  </head>
<body>

  <div class="menulateral">
    <div class="logo">
      <img src="../proyecto/20250906_163741.png" alt="Logo Luxy">
    </div>
    <hr>
    <ul>
      <li class="active">Inicio</li>
      <li>Formulario1</li>
      <li>Formulario2</li>
      <li>Formulario3</li>
      <li>Formulario4</li>
    </ul>
  </div>

  <div class="main">
    <div class="card">
      <h1>Gestión de factura venta</h1>

    
      <form action="INSERTAR_FACRURAV.PHP" method="post">
        <div class="form-group">
          <input type="text" name="cod_factura_v" placeholder="Código" required>
          <input type="text" name="fecha_factura_v" ="fecha" placeholder="Fecha de venta"
                            onfocus="this.type='date'"  
                            onblur="if(!this.value) this.type='text'">
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
              onclick="return confirm('¿Deseas eliminar este rol?>Eliminar</a>
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
 <script>
    const cantidad = document.getElementById("Cantidad");
    const precio = document.getElementById("Precio");
    const total = document.getElementById("total");

    function calcularTotal() {
    const cant = parseFloat(cantidad.value) || 0;
    const prec = parseFloat(precio.value) || 0;
      total.value = (cant * prec).toFixed(2); // 2 decimales
    }

    
    cantidad.addEventListener("input", calcularTotal);
    precio.addEventListener("input", calcularTotal);
</script>
