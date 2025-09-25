<?php
require_once "CONEXION.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_rol'];
$sql = "SELECT id_rol,nombre_rol,descripcion,estado
FROM Rol 
WHERE id_rol ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar rol</title> 
    <link rel="stylesheet" href="../CSS/CSS_EDITAR.css">
    <img src="" height="50PX">
</head> 
<body> 
<div class="container">
  <div class="formulario">
    <form action="ACTUALIZAR_ROL.php" method="post"> 
       <h1>Actualizar Rol</h1> 
        <input type="hidden" name="id_rol" value="<?php echo $data['id_rol']; ?>"> 
        <label for="nombre_rol">Nombre: </label> 
        <input type="text" name="nombre_rol" value="<?php echo $data['nombre_rol']; ?>" required> 
        <label for="descripcion">Descripcion: </label> 
        <input type="text" name="descripcion" value="<?php echo $data['descripcion']; ?>" required> 
        <label for="estado">Estado: </label> 
        <input type="text" name="estado" value="<?php echo $data['estado']; ?>" required> 
        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


