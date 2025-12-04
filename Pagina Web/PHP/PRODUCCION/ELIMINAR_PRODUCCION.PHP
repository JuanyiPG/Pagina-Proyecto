<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_PRODUCCION.php"; 

$id = $_GET['id_produccion']; 

$produccion = new PRODUCCION(); 
$produccion->ELIMINAR_PRODUCCION($id);  

header("Location: INDEX_PRODUCCION.php"); 
exit;
?>