<?php
require_once "CONEXION.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_producto_t'];
$sql = "SELECT id_producto_t,nombre_producto_t,descripcion_producto_t,categoria_produ_t,unidad_medida,estado_producto_t,id_produccion_fk_producto_terminado
FROM producto_terminado 
WHERE id_producto_t ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar producto terminado</title> 
    <link rel="stylesheet" href="../CSS/CSS_EDITAR.css">
    <img src="" height="50PX">

</head> 
<body> 
<div class="container">
  <div class="formulario">
    <form action="ACTUALIZAR_PT.php" method="post"> 
       <h1>Actualizar producto terminado</h1> 
        <input type="hidden" name="id_producto_t" value="<?php echo $data['id_producto_t']; ?>"> 
        <label for="nombre_producto_t">Nombre: </label> 
        <input type="text" name="nombre_producto_t" value="<?php echo $data['nombre_producto_t']; ?>" required> 
        <label for="descripcion_producto_t">Descripcion: </label> 
        <input type="text" name="descripcion_producto_t" value="<?php echo $data['descripcion_producto_t']; ?>" required> 
        <label for="categoria_produ_t">Categoria: </label> 
        <input type="text" name="categoria_produ_t" value="<?php echo $data['categoria_produ_t']; ?>" required> 
        <label for="unidad_medida">Unidad de medida:</label> 
        <input type="text" name="unidad_medida" value="<?php echo $data['unidad_medida']; ?>" required> 
        <label for="estado_producto_t">Estado:</label> 
        <input type="text" name="estado_producto_t" value="<?php echo $data['estado_producto_t']; ?>" required>
        <label for="id_produccion_fk_producto_terminado">numero de produccion:</label> 
        <input type="text" name="id_produccion_fk_producto_terminado" value="<?php echo $data['id_produccion_fk_producto_terminado']; ?>" required>

        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


