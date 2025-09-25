<?php
require_once "CONEXION.php";

$obj = new CONECTAR();
$conexion = $obj->conexion();

$id = $_GET['id_materia_p'];
$sql = "SELECT id_materia_p,nom_materia_p,color_materia_p,categoria_mp,tipo_material_materia_p,stock_actual_materia_p,stock_minimo_materia_p,descripcion_materia_p,estado_materia_p
FROM Materia_prima 
WHERE id_materia_p ='$id'";
$resultado = mysqli_query($conexion,$sql);
$data = mysqli_fetch_assoc($resultado);

?>

<!DOCTYPE html> 
<html lang="es"> 
<head> 
    <meta charset="UTF-8"> 
    <title>Editar Materia Prima</title> 
    <link rel="stylesheet" href="../CSS/CSS_EDITAR.css">
    <img src="" height="50PX">

</head> 
<body> 
<div class="container">
  <div class="formulario">
    <form action="ACTUALIZAR_MATERIAP.php" method="post"> 
       <h1>Actualizar Materia prima</h1> 
        <input type="hidden" name="id_materia_p" value="<?php echo $data['id_materia_p']; ?>"> 
        <label for="nom_materia_p">Nombre: </label> 
        <input type="text" name="nom_materia_p" value="<?php echo $data['nom_materia_p']; ?>" required> 
        <label for="color_materia_p">Color: </label> 
        <input type="text" name="color_materia_p" value="<?php echo $data['color_materia_p']; ?>" required> 
        <label for="categoria_mp">Categoria: </label> 
        <input type="text" name="categoria_mp" value="<?php echo $data['categoria_mp']; ?>" required> 
        <label for="tipo_material_materia_p">tipo de material:</label> 
        <input type="text" name="tipo_material_materia_p" value="<?php echo $data['tipo_material_materia_p']; ?>" required> 
        <label for="stock_actual_materia_p">Stock actual:</label> 
        <input type="text" name="stock_actual_materia_p" value="<?php echo $data['stock_actual_materia_p']; ?>" required>
        <label for="stock_minimo_materia_p">Stock minimo:</label> 
        <input type="text" name="stock_minimo_materia_p" value="<?php echo $data['stock_minimo_materia_p']; ?>" required>
        <label for="descripcion_materia_p">Descripcion:</label> 
        <input type="text" name="descripcion_materia_p" value="<?php echo $data['descripcion_materia_p']; ?>" required>
        <label for="estado_materia_p">Estado:</label> 
        <input type="text" name="estado_materia_p" value="<?php echo $data['estado_materia_p']; ?>" required>

        <button type="submit">Actualizar</button> 
    </form> 
  </div>

</div>
</body> 
</html>


