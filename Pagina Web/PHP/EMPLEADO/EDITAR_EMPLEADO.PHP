<?php
require_once "../CONFIG.PHP";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_emple'];
$sql = "SELECT id_emple,nom_emple,tel_emple,correo_emple,dir_emple,rh_emple,fecha_naci_emple,fecha_ing_emple,salari_emple,estado_emple,usuario,contraseña,id_rol_fk_emple
FROM Empleado 
WHERE id_emple ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar empleado</title> 
    <link rel="stylesheet" href="../../CSS/index.css">
    <img src="../IMG/logoB.png" height="100PX" style = "margin-left: 48%;">
</head> 
<body> 
<div class="container-1">
  <div class="formulario-1">
    <form action="ACTUALIZAR_EMPLEADO.php" method="post"> 
       <h1>Actualizar producto terminado</h1> 
        <input type="hidden" name="id_emple" value="<?php echo $data['id_emple']; ?>"> 
        <label for="nom_emple">Nombre: </label> 
        <input type="text" name="nom_emple" value="<?php echo $data['nom_emple']; ?>" required> 
        <label for="dir_emple">Direccion: </label> 
        <input type="text" name="dir_emple" value="<?php echo $data['dir_emple']; ?>" required> 
        <label for="tel_emple">Telefono:</label> 
        <input type="text" name="tel_emple" value="<?php echo $data['tel_emple']; ?>" required> 
        <label for="correo_emple">Correo:</label> 
        <input type="text" name="correo_emple" value="<?php echo $data['correo_emple']; ?>" required>
        <label for="rh_emple">Tipo de sangre: </label> 
        <input type="text" name="rh_emple" value="<?php echo $data['rh_emple']; ?>" required> 
        <label for="fecha_naci_emple">Fecha de Nacimiento:</label> 
        <input type="date" name="fecha_naci_emple" value="<?php echo $data['Fecha_naci_emple']; ?>" required>
        <label for="Fecha_ing_emple">Fecha de ingreso:</label> 
        <input type="date" name="fecha_ing_emple" value="<?php echo $data['fecha_ing_emple']; ?>" required>
        <label for="salario_empleado">Salario:</label> 
        <input type="text" name="salari_emple" value="<?php echo $data['salari_emple']; ?>" required>
        <label for="estado_emple">Estado:</label> 
        <input type="text" name="estado_emple" value="<?php echo $data['estado_emple']; ?>" required>
        <label for="usuario">Nombre de usuario:</label> 
        <input type="text" name="usuario" value="<?php echo $data['usuario']; ?>" required>
        <label for="contraseña">Contraseña:</label> 
        <input type="text" name="contraseña" value="<?php echo $data['contraseña']; ?>" required>
        <label for="id_rol_fk_emple">numero de rol:</label> 
        <input type="text" name="id_rol_fk_emple" value="<?php echo $data['id_rol_fk_emple']; ?>" required>

        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


