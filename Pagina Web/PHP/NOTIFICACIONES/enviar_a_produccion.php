<?php
header("Content-Type: application/json; charset=UTF-8");

if (!isset($_POST['id_pedido'])) {
    echo json_encode(["success" => false, "message" => "ID de pedido no recibido"]);
    exit;
}

$id_pedido   = $_POST['id_pedido'];
$nombre      = $_POST['nombre']      ?? "";
$talla       = $_POST['talla']       ?? "";
$color       = $_POST['color']       ?? "";
$categoria   = $_POST['categoria']   ?? "";
$material    = $_POST['material']    ?? "";
$cantidad    = $_POST['cantidad']    ?? "";
$descripcion = $_POST['descripcion'] ?? "";
$fecha       = $_POST['fecha']       ?? "";
$subtotal    = $_POST['subtotal']    ?? "";
$valor       = $_POST['valor']       ?? "";
$estado      = $_POST['estado']      ?? "";
$cliente     = $_POST['cliente']     ?? "";

// Ruta del archivo donde se guardarán los pedidos
$file = __DIR__ . "/produccion.json";

// Leer pedidos actuales
$pedidos = [];
if (file_exists($file)) {
    $json = file_get_contents($file);
    $pedidos = json_decode($json, true) ?? [];
}

// Agregar el nuevo pedido
$pedidos[] = [
    "id_pedido"   => $id_pedido,
    "nombre"      => $nombre,
    "talla"       => $talla,
    "color"       => $color,
    "categoria"   => $categoria,
    "material"    => $material,
    "cantidad"    => $cantidad,
    "descripcion" => $descripcion,
    "fecha"       => $fecha ?: date("Y-m-d H:i:s"),
    "subtotal"    => $subtotal,
    "valor"       => $valor,
    "estado"      => $estado,
    "cliente"     => $cliente
];

// Guardar de nuevo en el archivo
file_put_contents($file, json_encode($pedidos, JSON_PRETTY_PRINT));

echo json_encode([
    "success" => true,
    "message" => "Pedido $id_pedido enviado a producción"
]);


