<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_MATERIAP.php"; 

$id = $_GET['id_materia_p']; 

$materia_p = new MATERIA_P(); 
$materia_p->ELIMINAR_MATERIA_PRIMA($id);  

header("Location: INDEX_MATERIAP.php"); 
exit;
?>