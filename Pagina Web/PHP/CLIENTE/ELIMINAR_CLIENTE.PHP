<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_CLIENTE.php"; 

$id = $_GET['id_cliente']; 

$cliente = new CLIENTE(); 
$cliente->ELIMINAR_CLIENTE($id);  

header("Location: INDEX_CLIENTE.PHP"); 
exit;
?>