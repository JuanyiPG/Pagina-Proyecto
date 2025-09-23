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
    <img src="" height="50PX">
</head> 
<style>
body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 0;
    background-image: url("BACKROUND.3.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    height: 100%;
}

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.formulario {
    width: 400px;
    padding: 40px;
    border-radius: 20px;
    background-color: #f2f2f2;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 40px;
    position: relative;
}

.formulario h1 {
    font-size: 24px;
    margin-bottom: 20px;
    text-align: center;
    color: rgb(104, 10, 41);
}

.formulario label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #333;
}

.formulario input[type="text"], .formulario input[type="date"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 20px;
    margin-bottom: 20px;
    font-size: 14px;
    transition: all 0.3s ease;
}

.formulario input[type="text"]:focus, .formulario input[type="date"]:focus {
    border-color: rgb(104, 10, 41);
    outline: none;
}

.formulario button {
      margin-top: 10px;
      background: rgb(104, 10, 41);
      color: #fff;
      padding: 12px 25px;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      font-size: 15px;
      font-weight: bold;
      transition: 0.3s;
      display: block;
      margin-left: auto;
      margin-right: auto;
}

.formulario button:hover {
    background-color: #b33a3a;
}


</style>
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


