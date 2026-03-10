<?php
require_once "../CONFIG.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['cod_factura_v'];
$sql = "SELECT cod_factura_v,fecha_factura_v,sub_total_factura_v,iva_factura_v,total_factura_v,metodo_pago,descuento,estado_factura_venta,id_empleado_fk_factura
FROM Factura_Venta 
WHERE cod_factura_v ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar Factura Venta</title> 
    <link rel="stylesheet" href="../../CSS/index.css">
    <img src="" height="50PX">

</head> 
<body> 
<div class="container-1">
  <div class="formulario-1">
    <form action="ACTUALIZAR_FACTURAV.php" method="post"> 
       <h1>Actualizar Factura venta</h1> 
        <input type="hidden" name="cod_factura_v" value="<?php echo $data['cod_factura_v']; ?>"> 
        <label for="fecha_factura_v">Fecha: </label> 
        <input type="date" name="fecha_factura_v" value="<?php echo $data['fecha_factura_v']; ?>" required> 
        <label for="sub_total_factura_v">sub total: </label> 
        <input type="text" name="sub_total_factura_v" value="<?php echo $data['sub_total_factura_v']; ?>" required> 
        <label for="iva_factura_v">iva: </label> 
        <input type="text" name="iva_factura_v" value="<?php echo $data['iva_factura_v']; ?>" required> 
        <label for="total_factura_v">Total:</label> 
        <input type="text" name="total_factura_v" value="<?php echo $data['total_factura_v']; ?>" required> 
        <label for="metodo_pago">Metodo de pago:</label> 
        <input type="text" name="metodo_pago" value="<?php echo $data['metodo_pago']; ?>" required>
        <label for="descuento">Descuento:</label> 
        <input type="text" name="descuento" value="<?php echo $data['descuento']; ?>" required>
        <label for="estado_factura_venta">Descuento:</label> 
        <input type="text" name="estado_factura_venta" value="<?php echo $data['estado_factura_venta']; ?>" required>
       <label for="id_empleado_fk_factura">Numero de empleado que ingreso la factura:</label> 
        <input type="text" name="id_empleado_fk_factura" value="<?php echo $data['id_empleado_fk_factura']; ?>" required>
       
        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


