<?php

require_once "../CONFIG.PHP"; 
require_once "CLASE_EMPLEADO.php"; 

$id_empleado = $_POST['id_emple'];
$nom_empleado = $_POST['nom_emple'];
$telefono_empleado = $_POST['tel_emple'];
$correo_empleado = $_POST['correo_emple'];
$direccion_empleado = $_POST['dir_emple'];
$tipo_sangre = $_POST['rh_emple'];
$Fecha_nacim_empleado = $_POST['fecha_naci_emple'];
$Fecha_ing_empleado = $_POST['fecha_ing_emple'];
$salario_empleado = $_POST['salari_emple'];
$Estado_empleado = $_POST['estado_emple'];
$nom_usuario = $_POST['usuario'];
$contras = $_POST['contraseña'];
$id_rol_fk_empleado = $_POST['id_rol_fk_emple'];


$datos_empleado = array ($id_empleado, $nom_empleado, $telefono_empleado, $correo_empleado,$direccion_empleado,
$tipo_sangre, $Fecha_nacim_empleado, $Fecha_ing_empleado, $salario_empleado, $Estado_empleado,
$nom_usuario,$contras,$id_rol_fk_empleado);

$obj = new EMPLEADO();

if ($obj->INSERT_EMPLEADO($datos_empleado) == 1) 
{
    header("Location: INDEX_EMPLEADO.php");
} else 
{
    echo "Error al insertar datos del Epleado";
}
?>