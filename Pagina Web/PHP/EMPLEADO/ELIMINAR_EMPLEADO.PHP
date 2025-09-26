<?php 
require_once "CONEXION.php"; 
require_once "CLASE_EMPLEADO.php"; 

$id = $_GET['id_empleado']; 

$empleado = new EMPLEADO(); 
$empleado->ELIMINAR_EMPLEADO($id);  

header("Location: INDEX_EMPLEADO.php"); 
exit;
?>