<?php

require_once "../CONFIG.php"; 
require_once "CLASE_ROL.php"; 

$id_rol = $_POST['id_rol'];
$nombre_rol = $_POST['nom_rol'];
$descripcion = $_POST['desc_rol'];



$datos_rol = array($id_rol, $nombre_rol, $descripcion);

$obj = new ROL();

if($obj->existeRol($id_rol)){
    echo "<script>
            alert('ESE ROL YA EXISTE.');
            window.location.href = 'INDEX_ROL.php';
        </script>";;
}else{
    $datos_rol = array($id_rol, $nombre_rol, $descripcion);
    if ($obj->INSERT_ROL($datos_rol) == 1) 
{
    header("Location: INDEX_ROL.php");
} else 
{
    echo "Error al insertar datos del rol";
}
}
?>