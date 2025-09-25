<?php

require_once "CONEXION.php"; 
require_once "CLASE_PEDIDO.PHP"; 

$id_pedido = $_POST['id_pedido'];
$nom_p_edido = $_POST['nom_p_edido'];
$talla_p_pedido = $_POST['talla_p_pedido'];
$color_p_pedido = $_POST['color_p_pedido'];
$categoria_p_pedido = $_POST['categoria_p_pedido'];
$material_p_pedido = $_POST['material_p_pedido'];
$cant_producto = $_POST['cant_producto'];
$descripcion_p_pedido = $_POST['descripcion_p_pedido'];
$fecha_pedido = $_POST['fecha_pedido'];
$sub_total_pedido = $_POST['sub_total_pedido'];
$valor_pedido = $_POST['valor_pedido'];
$estado_pedido = $_POST['estado_pedido'];
$id_cliente_fk_pedido = $_POST['id_cliente_fk_pedido'];


$datos_pedido = array($id_pedido, $nom_p_edido, $talla_p_pedido,
$color_p_pedido, $categoria_p_pedido, $material_p_pedido, $cant_producto, $descripcion_p_pedido, 
$fecha_pedido, $sub_total_pedido, $valor_pedido,$estado_pedido, $id_cliente_fk_pedido);

$obj = new PEDIDO();

if ($obj->INSERT_PEDIDO($datos_pedido) == 1) 
{
    header("Location: INDEX_PEDIDO.php");
} else 
{
    echo "Error al insertar datos de el pedido";
}
?>