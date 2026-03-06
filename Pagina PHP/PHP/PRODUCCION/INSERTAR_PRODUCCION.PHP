<?php

require_once "../CONFIG.php"; 
require_once "CLASE_PRODUCCION.PHP"; 

$id_produccion = $_POST['id_produccion'];
$fecha_inicio_produccion = $_POST['fecha_inicio_produccion'];
$cantidad_producida = $_POST['cantidad_producida'];
$costo_mano_obra = $_POST['costo_mano_obra'];
$costo_total_materia_prima = $_POST['costo_total_materia_prima'];
$costo_iva = $_POST['costo_iva'];
$costo_total_produccion = $_POST['costo_total_produccion'];
$fecha_fin_produccion = $_POST['fecha_fin_produccion'];
$estado_produccion = $_POST['estado_produccion'];
$id_empleado_fk_produccion = $_POST['id_empleado_fk_produccion'];
$id_pedido_fk_produccion = $_POST['id_pedido_fk_produccion'];

$datos_produccion = array($id_produccion, $fecha_inicio_produccion, $cantidad_producida,
$costo_mano_obra, $costo_total_materia_prima, $costo_iva, $costo_total_produccion, $fecha_fin_produccion, 
$estado_produccion, $id_empleado_fk_produccion, $id_pedido_fk_produccion);

$obj = new PRODUCCION();

if ($obj->INSERT_PRODUCCION($datos_produccion) == 1) 
{
    header("Location: INDEX_PRODUCCION.php");
} else 
{
    echo "Error al insertar datos de la Produccion";
}
?>