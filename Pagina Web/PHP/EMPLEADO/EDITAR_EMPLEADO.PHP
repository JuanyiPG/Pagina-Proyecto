<?php
require_once "../CONFIG.PHP";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_empleado'];
$sql = "SELECT id_empleado,nom_empleado,direccion_empleado,tipo_sangre,telefono_empleado,correo_empleado,Fecha_ing_empleado,salario_empleado,Estado_empleado,nom_usuario,contras,id_rol_fk_empleado
FROM Empleado 
WHERE id_empleado ='$id'";
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
        <input type="hidden" name="id_empleado" value="<?php echo $data['id_empleado']; ?>"> 
        <label for="nom_empleado">Nombre: </label> 
        <input type="text" name="nom_empleado" value="<?php echo $data['nom_empleado']; ?>" required> 
        <label for="direccion_empleado">Direccion: </label> 
        <input type="text" name="direccion_empleado" value="<?php echo $data['direccion_empleado']; ?>" required> 
        <label for="tipo_sangre">Tipo de sangre: </label> 
        <input type="text" name="tipo_sangre" value="<?php echo $data['tipo_sangre']; ?>" required> 
        <label for="telefono_empleado">Telefono:</label> 
        <input type="text" name="telefono_empleado" value="<?php echo $data['telefono_empleado']; ?>" required> 
        <label for="correo_empleado">Correo:</label> 
        <input type="text" name="correo_empleado" value="<?php echo $data['correo_empleado']; ?>" required>
        <label for="Fecha_ing_empleado">Fecha de ingreso:</label> 
        <input type="date" name="Fecha_ing_empleado" value="<?php echo $data['Fecha_ing_empleado']; ?>" required>
        <label for="salario_empleado">Salario:</label> 
        <input type="text" name="salario_empleado" value="<?php echo $data['salario_empleado']; ?>" required>
        <label for="Estado_empleado">Estado:</label> 
        <input type="text" name="Estado_empleado" value="<?php echo $data['Estado_empleado']; ?>" required>
        <label for="nom_usuario">Nombre de usuario:</label> 
        <input type="text" name="nom_usuario" value="<?php echo $data['nom_usuario']; ?>" required>
        <label for="contras">Contraseña:</label> 
        <input type="text" name="contras" value="<?php echo $data['contras']; ?>" required>
        <label for="id_rol_fk_empleado">numero de rol:</label> 
        <input type="text" name="id_rol_fk_empleado" value="<?php echo $data['id_rol_fk_empleado']; ?>" required>

        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


