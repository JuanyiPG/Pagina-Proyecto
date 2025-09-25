<?php
require_once "CONEXION.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_produccion'];
$sql = "SELECT id_produccion,fecha_inicio_produccion,cantidad_producida,costo_mano_obra,costo_total_materia_prima,costo_iva,costo_total_produccion,fecha_fin_produccion,estado_produccion,id_empleado_fk_produccion,id_pedido_fk_produccion
FROM Produccion 
WHERE id_produccion ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar Produccion</title> 
    <link rel="stylesheet" href="../CSS/CSS_EDITAR.css">
    <img src="" height="50PX">

</head> 
<body> 
<div class="container">
  <div class="formulario">
    <form action="ACTUALIZAR_PRODUCCION.php" method="post"> 
       <h1>Actualizar produccion</h1> 
        <input type="hidden" name="id_produccion" value="<?php echo $data['id_produccion']; ?>"> 
        <label for="fecha_inicio_produccion">Fecha inicio: </label> 
        <input type="date" name="fecha_inicio_produccion" value="<?php echo $data['fecha_inicio_produccion']; ?>" required> 
        <label for="costo_mano_obra">Costo de mano de obra: </label> 
        <input type="text" name="costo_mano_obra" value="<?php echo $data['costo_mano_obra']; ?>" required> 
        <label for="cantidad_producida">Cantidad: </label> 
        <input type="text" name="cantidad_producida" value="<?php echo $data['cantidad_producida']; ?>" required> 
        <label for="costo_total_materia_prima">Costo de el material tota utilizado: </label> 
        <input type="text" name="costo_total_materia_prima" value="<?php echo $data['costo_total_materia_prima']; ?>" required> 
        <label for="costo_iva">IVA:</label> 
        <input type="text" name="costo_iva" value="<?php echo $data['costo_iva']; ?>" required> 
        <label for="costo_total_produccion">Costo final:</label> 
        <input type="text" name="costo_total_produccion" value="<?php echo $data['costo_total_produccion']; ?>" required>
        <label for="fecha_fin_produccion">Fecha de finalizacion:</label> 
        <input type="date" name="fecha_fin_produccion" value="<?php echo $data['fecha_fin_produccion']; ?>" required>
        <label for="estado_produccion">Estado:</label> 
        <input type="text" name="estado_produccion" value="<?php echo $data['estado_produccion']; ?>" required>
       <label for="id_empleado_fk_produccion">Numero de empleado que registro la produccion:</label> 
        <input type="text" name="id_empleado_fk_produccion" value="<?php echo $data['id_empleado_fk_produccion']; ?>" required>
        <label for="id_pedido_fk_produccion">Numero de el pedido de la produccion:</label> 
        <input type="text" name="id_pedido_fk_produccion" value="<?php echo $data['id_pedido_fk_produccion']; ?>" required>

        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


