<?php

require_once "../CONFIG.PHP"; 
require_once "CLASE_EMPLEADO.php"; 

$id_empleado = $_POST['id_empleado'];
$nom_empleado = $_POST['nom_empleado'];
$direccion_empleado = $_POST['direccion_empleado'];
$tipo_sangre = $_POST['tipo_sangre'];
$telefono_empleado = $_POST['telefono_empleado'];
$correo_empleado = $_POST['correo_empleado'];
$Fecha_ing_empleado = $_POST['Fecha_ing_empleado'];
$salario_empleado = $_POST['salario_empleado'];
$Estado_empleado = $_POST['Estado_empleado'];
$nom_usuario = $_POST['nom_usuario'];
$contras = $_POST['contras'];
$id_rol_fk_empleado = $_POST['id_rol_fk_empleado'];


$datos_empleado = array ($id_empleado, $nom_empleado, $direccion_empleado,
$tipo_sangre,$telefono_empleado, $correo_empleado, $Fecha_ing_empleado, $salario_empleado, $Estado_empleado,
$nom_usuario,$contras,$id_rol_fk_empleado);

$obj = new EMPLEADO();

if ($obj-> ACTUALIZAR_EMPLEADO($datos_empleado)) 
{
    header("location:INDEX_EMPLEADO.php");
    exit;
} 
else 
{
    echo "Error al actualizar datos del EMPLEADO";
}
?>