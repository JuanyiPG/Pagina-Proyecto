<?php 
require_once "CONEXION.php"; 
require_once "CLASE_ROL.php";  

$datos = [];
$obj = new ROL();
    
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $datos = $obj->ConsultarProducto_tPorID($search); 
} else {
    $datos = $obj->CONSULTAR_ROL(); 
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Roles</title>
  <link rel="stylesheet" href="../CSS/CSS.css">
  </head>
<body>

  <div class="menulateral">
    <div class="logo">
      <img src="../proyecto/20250906_163741.png" alt="Logo Luxy">
    </div>
    <hr>
    <ul>
      <li class="active">Inicio</li>
      <li>Formulario1</li>
      <li>Formulario2</li>
      <li>Formulario3</li>
      <li>Formulario4</li>
    </ul>
  </div>

  <div class="main">
    <div class="card">
      <h1>Gestión de roles</h1>

     
      <form action="INSERTAR_ROL.php" method="post">
        <div class="form-group">
          <input type="text" name="id_rol" placeholder="Código" required>
          <input type="text" name="nombre_rol" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="descripcion" placeholder="Descripcion">
        </div>
        <div class="form-group">
          <input type="text" name="estado" placeholder="Estado">
        </div>
        <button type="submit" class="save-btn">Insertar</button>
      </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nombre</th>
          <th>Descripcion</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_rol']; ?></td>
            <td><?php echo $row['nombre_rol']; ?></td>
            <td><?php echo $row['descripcion']; ?></td>
            <td><?php echo $row['estado']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_ROL.php?id_rol=<?php echo $row['id_rol']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_ROL.php?id_rol=<?php echo $row['id_rol']; ?>">Eliminar</a>
            </td>
          </tr>
        <?php } ?>
      </tbody>
    </table>
  </div>

</body>
</html>
