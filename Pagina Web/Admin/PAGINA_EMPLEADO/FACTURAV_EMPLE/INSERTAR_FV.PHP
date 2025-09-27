<?php

require_once "../FACTURAV_EMPLE/CONEXION.PHP"; 
require_once "../FACTURAV_EMPLE/CLASE_FV.PHP";  


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

if ($obj->INSERT_FACTURA_V($datos_factura_v) == 1) 
{
    header("Location: ../FACTURAV_EMPLE/INDEX_FACTURA_EMPLE.php");
} else 
{
    echo "Error al insertar datos de la factura venta";
}
?>