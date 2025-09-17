<?php

require_once "CONEXION.php"; 
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

if ($obj->INSERT_PRODUCTO_T($datos_producto_t) == 1) 
{
    header("Location: INDEX_PRODUCTOT.php");
} else 
{
    echo "Error al insertar datos del El producto terminado";
}
?>
