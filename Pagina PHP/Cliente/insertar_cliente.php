<?php

require_once "../PHP/CONFIG.php"; 
require_once "clase_cliente.php"; 

$id_pedido = 1;
$nom_p_edido = "Blusa camisa de hombro";
$talla_p_pedido = $_POST['talla'];
$color_p_pedido = $_POST['color'];
$categoria_p_pedido = $_POST['categoria'];
$material_p_pedido = $_POST['material'];
$cant_producto = $_POST['cantidad'];
$descripcion_p_pedido = $_POST['descripcion'];
$fecha_pedido = date("Y-m-d");
$sub_total_pedido = $valor * $cantidad;
$valor_pedido = $_POST['valor'] ?? 0;
$estado_pedido = "pendiente";
$id_cliente_fk_pedido = $_POST['1'];


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