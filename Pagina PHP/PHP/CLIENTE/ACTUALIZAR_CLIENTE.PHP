<?php

require_once "../CONFIG.php"; 
require_once "CLASE_CLIENTE.php"; 

$id_cliente = $_POST['id_cliente'];
$nom_cliente = $_POST['nom_cliente'];
$direccion_cliente = $_POST['direccion_cliente'];
$telefono_cliente = $_POST['telefono_cliente'];
$correo_cliente = $_POST['correo_cliente'];
$nombre_usuari = $_POST['nombre_usuari'];
$contra = $_POST['contra'];
$id_rol_fk_cliente = $_POST['id_rol_fk_cliente'];


$datos_cliente = array($id_cliente, $nom_cliente, $direccion_cliente,
$telefono_cliente, $correo_cliente,$nombre_usuari,$contra, $id_rol_fk_cliente);

$obj = new CLIENTE();

if ($obj-> ACTUALIZAR_CLIENTE($datos_cliente)) 
{
    header("location:INDEX_CLIENTE.PHP");
    exit;
} 
else 
{
    echo "Error al actualizar datos del CLIENTE";
}
?>