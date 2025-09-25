<?php 
require_once "CONEXION.php"; 
require_once "CLASE_ROL.php"; 

$id = $_GET['id_rol']; 

$rol = new ROL(); 
$rol->ELIMINAR_ROLi($id);  

header("Location: INDEX_ROL.php"); 
exit;
?>