<?php

require_once "../CONFIG.php"; 
require_once "CLASE_PRODUCTO_T.php"; 

$id_producto_t = $_POST['id_producto_t'];
$nombre_producto_t = $_POST['nombre_producto_t'];
$descripcion_producto_t = $_POST['descripcion_producto_t'];
$categoria_produ_t = $_POST['categoria_produ_t'];
$unidad_medida = $_POST['unidad_medida'];
$estado_producto_t = $_POST['estado_producto_t'];
$id_produccion_fk_producto_terminado = $_POST['id_produccion_fk_producto_terminado'];


$datos_producto_t = array($id_producto_t, $nombre_producto_t, $descripcion_producto_t,
$categoria_produ_t, $unidad_medida, $estado_producto_t, $id_produccion_fk_producto_terminado);

$obj = new PRODUCTO_T();

if ($obj-> ACTUALIZAR($datos_producto_t)) 
{
    header("location:INDEX_PRODUCTOT.php");
    exit;
} 
else 
{
    echo "Error al actualizar datos del PRODUCTO TERMINADO";
}
?>