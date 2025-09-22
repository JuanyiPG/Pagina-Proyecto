<?php 
require_once "CONEXION.php"; 
require_once "CLASE_PRODUCTO_T.php"; 

$id = $_GET['id_producto_t']; 

$producto_t = new PRODUCTO_T(); 
$producto_t->ELIMINAR($id);  

header("Location: INDEX_PRODUCTOT.php"); 
exit;
?>
