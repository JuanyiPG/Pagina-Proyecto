<?php

require_once "../CLIENTE/CONEXION.PHP"; 
require_once "../Login/CLASE_REGISTRO.PHP"; 

$id_cliente = $_POST['id_cliente'];
$nom_cliente = $_POST['nom_cliente'];
$direccion_cliente = $_POST['direccion_cliente'];
$telefono_cliente = $_POST['telefono_cliente'];
$correo_cliente = $_POST['correo_cliente'];
$nombre_usuari = $_POST['nombre_usuari'];
$contra = $_POST['contra'];
$id_rol_fk_cliente = $_POST['id_rol_fk_cliente'];


$datos_registro = array($id_cliente, $nom_cliente, $direccion_cliente,
$telefono_cliente, $correo_cliente,$nombre_usuari,$contra, $id_rol_fk_cliente);

$obj = new CLIENTE();

if ($obj->INSERT_CLIENTE($datos_registro) == 1) {
    header("Location: ../Login/registro.php?mensaje=ok");
    exit();
} else {
    header("Location: ../Login/registro.php?mensaje=error");
    exit();
}
?>