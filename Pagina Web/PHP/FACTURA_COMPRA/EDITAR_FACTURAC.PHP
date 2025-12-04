<?php
require_once "../CONFIG.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['cod_factura_compra'];
$sql = "SELECT cod_factura_compra,fecha_factura_compra,total_faactura_compra,metododepago_factura_compra,estado_factura_compra,id_empleado_fk_factura_compra
FROM Factura_compra 
WHERE cod_factura_compra ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar Factura compra</title> 
    <link rel="stylesheet" href="../../CSS/index.css">
    <img src="" height="50PX">

</head> 
<body> 
<div class="container-1">
  <div class="formulario-1">
    <form action="ACTUALIZAR_FACTURAC.php" method="post"> 
       <h1>Actualizar factura compra</h1> 
        <input type="hidden" name="cod_factura_compra" value="<?php echo $data['cod_factura_compra']; ?>"> 
        <label for="fecha_factura_compra">Fecha: </label> 
        <input type="date" name="fecha_factura_compra" value="<?php echo $data['fecha_factura_compra']; ?>" required> 
        <label for="total_faactura_compra">Total: </label> 
        <input type="text" name="total_faactura_compra" value="<?php echo $data['total_faactura_compra']; ?>" required> 
        <label for="metododepago_factura_compra">Metodo de pago: </label> 
        <input type="text" name="metododepago_factura_compra" value="<?php echo $data['metododepago_factura_compra']; ?>" required> 
        <label for="estado_factura_compra">Estado:</label> 
        <input type="text" name="estado_factura_compra" value="<?php echo $data['estado_factura_compra']; ?>" required> 
        <label for="id_empleado_fk_factura_compra">Numero de el empleado que registro la factura:</label> 
        <input type="text" name="id_empleado_fk_factura_compra" value="<?php echo $data['id_empleado_fk_factura_compra']; ?>" required>
       
        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


