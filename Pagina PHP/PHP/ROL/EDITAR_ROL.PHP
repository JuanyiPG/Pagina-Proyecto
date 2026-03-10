<?php
require_once "../CONFIG.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_rol'];
$sql = "SELECT id_rol,nom_rol,desc_rol
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
    <link rel="stylesheet" href="../../CSS/index.css">
    <img src="" height="50PX">
</head> 
<body class= "body"> 
<div class="container-1">
  <div class="formulario-1">
    <form action="ACTUALIZAR_ROL.php" method="post"> 
       <h1>Actualizar Rol</h1> 
        <input type="hidden" name="id_rol" value="<?php echo $data['id_rol']; ?>"> 
        <label for="nom_rol">Nombre: </label> 
        <input type="text" name="nom_rol" value="<?php echo $data['nom_rol']; ?>" required> 
        <label for="desc_rol">Descripcion: </label> 
        <input type="text" name="desc_rol" value="<?php echo $data['desc_rol']; ?>" required> 
        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


