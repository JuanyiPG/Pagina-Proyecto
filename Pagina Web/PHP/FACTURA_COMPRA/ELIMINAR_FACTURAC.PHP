<?php 
require_once "CONEXION.php"; 
require_once "CLASE_FACTURAC.php"; 

$id = $_GET['cod_factura_compra']; 

$factura_c = new FACTURA_C(); 
$factura_c->ELIMINAR_FACTURA_C($id);  

header("Location: INDEX_FACTURAC.php"); 
exit;
?>