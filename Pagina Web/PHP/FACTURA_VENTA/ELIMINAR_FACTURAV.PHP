<?php 
require_once "CONEXION.php"; 
require_once "CLASE_FACTURAV.php"; 

$id = $_GET['cod_factura_v']; 

$factura_v = new FACTURA_V(); 
$factura_v->ELIMINAR_FACTURA_V($id);  

header("Location: INDEX_FACTURAV.php"); 
exit;
?>