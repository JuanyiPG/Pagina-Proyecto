<?php
require_once "../CONFIG.php"; // Ajusta ruta según tu proyecto
$con = new CONECTAR();
$conexion = $con->conexion();

// Supongamos que tienes una tabla notificacion con estado "pendiente"
$sql = "SELECT COUNT(*) AS total FROM notificacion WHERE estado = 'pendiente'";
$result = $conexion->query($sql);
$data = $result->fetch_assoc();

echo $data['total'];
