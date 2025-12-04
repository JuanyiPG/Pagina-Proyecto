<?php

require_once "../CONFIG.php"; 
require_once "CLASE_FACTURAC.PHP"; 

$cod_factura_compra = $_POST['cod_factura_compra'];
$fecha_factura_compra = $_POST['fecha_factura_compra'];
$total_faactura_compra = $_POST['total_faactura_compra'];
$metododepago_factura_compra = $_POST['metododepago_factura_compra'];
$estado_factura_compra = $_POST['estado_factura_compra'];
$id_empleado_fk_factura_compra = $_POST['id_empleado_fk_factura_compra'];

$datos_factura_c = array($cod_factura_compra, $fecha_factura_compra, $total_faactura_compra,
$metododepago_factura_compra, $estado_factura_compra, $id_empleado_fk_factura_compra);

$obj = new FACTURA_C();

if ($obj->INSERT_FACTURA_C($datos_factura_c) == 1) 
{
    header("Location: INDEX_FACTURAC.php");
} else 
{
    echo "Error al insertar datos de la factura compra";
}
?>