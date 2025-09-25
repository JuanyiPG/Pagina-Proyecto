<?php

require_once "CONEXION.php"; 
require_once "CLASE_FACTURAC.php"; 

$cod_factura_compra = $_POST['cod_factura_compra'];
$fecha_factura_compra = $_POST['fecha_factura_compra'];
$total_faactura_compra = $_POST['total_faactura_compra'];
$metododepago_factura_compra = $_POST['metododepago_factura_compra'];
$estado_factura_compra = $_POST['estado_factura_compra'];
$id_empleado_fk_factura_compra = $_POST['id_empleado_fk_factura_compra'];

$datos_factura_c = array($cod_factura_compra, $fecha_factura_compra, $total_faactura_compra,
$metododepago_factura_compra, $estado_factura_compra, $id_empleado_fk_factura_compra);

$obj = new FACTURA_C();

if ($obj-> ACTUALIZAR_FACTURA_C($datos_factura_c)) 
{
    header("location:INDEX_FACTURAC.php");
    exit;
} 
else 
{
    echo "Error al actualizar datos de la factura compra";
}
?>