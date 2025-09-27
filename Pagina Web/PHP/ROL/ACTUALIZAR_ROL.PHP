<?php

require_once "../CONFIG.php"; 
require_once "CLASE_ROL.php"; 

$id_rol = $_POST['id_rol'];
$nombre_rol = $_POST['nombre_rol'];
$descripcion = $_POST['descripcion'];
$estado = $_POST['estado'];


$datos_rol = array($id_rol, $nombre_rol, $descripcion, $estado);

$obj = new ROL();

if ($obj-> ACTUALIZAR_ROL($datos_rol)) 
{
    header("location:INDEX_ROL.php");
    exit;
} 
else 
{
    echo "Error al actualizar datos del ROL";
}
?>