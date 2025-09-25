<?php

require_once "CONEXION.php"; 
require_once "CLASE_MATERIAP.php"; 

$id_materia_p = $_POST['id_materia_p'];
$nom_materia_p = $_POST['nom_materia_p'];
$color_materia_p = $_POST['color_materia_p'];
$categoria_mp = $_POST['categoria_mp'];
$tipo_material_materia_p = $_POST['tipo_material_materia_p'];
$stock_actual_materia_p = $_POST['stock_actual_materia_p'];
$stock_minimo_materia_p = $_POST['stock_minimo_materia_p'];
$descripcion_materia_p = $_POST['descripcion_materia_p'];
$estado_materia_p = $_POST['estado_materia_p'];


$datos_materia_p = array($id_materia_p, $nom_materia_p, $color_materia_p,
$categoria_mp, $tipo_material_materia_p, $stock_actual_materia_p, $stock_minimo_materia_p, $descripcion_materia_p, $estado_materia_p);

$obj = new MATERIA_P();

if ($obj-> ACTUALIZAR_MATERIA_P($datos_materia_p)) 
{
    header("location:INDEX_MATERIAP.php");
    exit;
} 
else 
{
    echo "Error al actualizar datos de la materia prima";
}
?>