<?php

require_once "../CONFIG.php"; 
require_once "CLASE_ROL.php"; 

$id_rol = $_POST['id_rol'];
$nombre_rol = $_POST['nombre_rol'];
$descripcion = $_POST['descripcion'];
$estado = $_POST['estado'];

$datos_rol = array($id_rol, $nombre_rol, $descripcion, $estado);

$obj = new ROL();

if ($obj->INSERT_ROL($datos_rol) == 1) 
{
    header("Location: INDEX_ROL.php");
} else 
{
    echo "Error al insertar datos del rol";
}
?>