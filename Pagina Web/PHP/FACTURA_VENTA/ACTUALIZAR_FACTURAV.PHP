<?php

require_once "../CONFIG.php"; 
require_once "CLASE_FACTURAV.php"; 

$cod_factura_v = $_POST['cod_factura_v'];
$fecha_factura_v = $_POST['fecha_factura_v'];
$sub_total_factura_v = $_POST['sub_total_factura_v'];
$iva_factura_v = $_POST['iva_factura_v'];
$total_factura_v = $_POST['total_factura_v'];
$metodo_pago = $_POST['metodo_pago'];
$descuento = $_POST['descuento'];
$estado_factura_venta = $_POST['estado_factura_venta'];
$id_empleado_fk_factura = $_POST['id_empleado_fk_factura'];

$datos_factura_v = array($cod_factura_v, $fecha_factura_v, $sub_total_factura_v,
$iva_factura_v, $total_factura_v, $metodo_pago, $descuento, $estado_factura_venta, $id_empleado_fk_factura);

$obj = new FACTURA_V();

if ($obj-> ACTUALIZAR_FACTURA_v($datos_factura_v)) 
{
    header("location:INDEX_FACTURAV.php");
    exit;
} 
else 
{
    echo "Error al actualizar datos de la factura venta";
}
?>