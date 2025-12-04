<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_PEDIDO.php"; 

$id = $_GET['id_pedido']; 

$pedido = new PEDIDO(); 
$pedido->ELIMINAR_PEDIDO($id);  

header("Location: INDEX_PEDIDO.php"); 
exit;
?>