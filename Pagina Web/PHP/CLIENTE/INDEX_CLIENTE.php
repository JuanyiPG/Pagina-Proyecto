<?php 
require_once "CONEXION.php"; 
require_once "CLASE_CLIENTE.php";  

$datos = [];
$obj = new CLIENTE();
    
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $datos = $obj->Consultarcliente_tPorID($search); 
} else {
    $datos = $obj->CONSULTAR_CLIENTE(); 
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gestion CLientes</title>
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
      <h1>Gestión Clientes</h1>

     
      <form action="INSERTAR_CLIENTE.php" method="post">
        <div class="form-group">
          <input type="text" name="id_cliente" placeholder="Código" required>
          <input type="text" name="nom_cliente" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="direccion_cliente" placeholder="Direccion"required>
        </div>
        <div class="form-group">
          <input type="text" name="telefono_cliente" placeholder="telefono"required>
        </div>
        <div class="form-group">
          <input type="text" name="correo_cliente" placeholder="Correo"required>
          <input type="text" name="id_rol_fk_cliente" placeholder="Numero de rol"required>
        </div>
        <button type="submit" class="save-btn">Insertar</button>
      </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nombre</th>
          <th>Direccion</th>
          <th>Telefono</th>
          <th>Correo</th>
          <th>Numero de rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_cliente']; ?></td>
            <td><?php echo $row['nom_cliente']; ?></td>
            <td><?php echo $row['direccion_cliente']; ?></td>
            <td><?php echo $row['telefono_cliente']; ?></td>
            <td><?php echo $row['correo_cliente']; ?></td>
            <td><?php echo $row['id_rol_fk_cliente']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_CLIENTE.php?id_cliente=<?php echo $row['id_cliente']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_CLIENTE.php?id_cliente=<?php echo $row['id_cliente']; ?>">Eliminar</a>
            </td>
          </tr>
        <?php } ?>
      </tbody>
    </table>
  </div>

</body>
</html>
