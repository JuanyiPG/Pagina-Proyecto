<?php
// Conexión a la BD
$conn = new mysqli("localhost", "root", "Basededatos321", "BASE_DE_DATOS");

if ($conn->connect_error) {
    die("Error en conexión: " . $conn->connect_error);
}

// Recibir los datos del formulario
$id = $_POST['Id'];
$fecha = $_POST['Fecha'];
$categoria = $_POST['Cat'];
$material = $_POST['material'] ?? null;
$insumos = $_POST['Insumos'] ?? null;
$ubicacion = $_POST['Ubicacion'];
$color = $_POST['Color'];
$uniMed = $_POST['UniMed'];
$cantidad = $_POST['Cant'];
$precio = $_POST['Precio'];
$destino = $_POST['Destino'];

// Calcular total en PHP también
$total = $cantidad * $precio;
echo= $total

// Guardar en BD
$sql = "INSERT INTO insrt_Materia_prima (id_materia, Nom_materia_prima, Tipo_material, Color, Stock_actual, Descripcion,) 
        VALUES ('$id','$material', '$categoria', '$color','$cantidad', '$insumos')";

if ($conn->query($sql) === TRUE) {
    echo "✅ Registro guardado correctamente";
} else {
    echo "❌ Error: " . $conn->error;
}

$conn->close();
?>