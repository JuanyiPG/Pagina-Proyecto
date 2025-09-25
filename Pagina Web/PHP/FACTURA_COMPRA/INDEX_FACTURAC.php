<?php 
require_once "CONEXION.php"; 
require_once "CLASE_FACTURAC.PHP";  

$datos = [];
$obj = new FACTURA_C();
    
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $datos = $obj->ConsultarfacturactPorID($search); 
} else {
    $datos = $obj->CONSULTAR_FACTURA_C(); 
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fctura compra</title>
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
      <h1>Gestión de factura compra</h1>

     
      <form action="INSERTAR_FACRURAC.PHP" method="post">
        <div class="form-group">
          <input type="text" name="cod_factura_compra" placeholder="Código" required>
          <input type="text" name="fecha_factura_compra" ="fecha" placeholder="Fecha de compra"
                            onfocus="this.type='date'"  
                            onblur="if(!this.value) this.type='text'">
        </div>
        <div class="form-group">
          <input type="text" name="total_faactura_compra" placeholder="total de la factura"required>
          <input type="text" name="metododepago_factura_compra" placeholder="Metodo de pago"required>
        </div>
        <div class="form-group">
          <input type="text" name="estado_factura_compra" placeholder="Estado"required>
          <input type="text" name="id_empleado_fk_factura_compra" placeholder="Identificador de el empleado que regustro la factura compra"required>
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
      </tbody>
    </table>
                  <?php } ?>
<?php } else { ?>
    <tr><td colspan="5">No se encontraron resultados</td></tr>
<?php } ?>
  </div>

</body>
</html>