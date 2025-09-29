<?php 
require_once "../CONFIG.PHP"; 
require_once "CLASE_EMPLEADO.php";  

$datos = [];
$obj = new EMPLEADO();
    
$search = (isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_EMPLEADO($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Producto terminado</title>
  <link rel="stylesheet" href="../../CSS/index.css">
  <body class="body2">


  <div class="main">
    <div class="card">
      <h1>Gestión de Empleados</h1>

     
      <form action="INSERTAR_EMPLEADO.php" method="post">
        <div class="form-group">
          <input type="text" name="id_empleado" placeholder="Código" required>
          <input type="text" name="nom_empleado" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="direccion_empleado" placeholder="Direccion">
          <input type="text" name="tipo_sangre" placeholder="tipo de sangre">
        </div>
        <div class="form-group">
          <input type="text" name="telefono_empleado" placeholder="Telefono">
          <input type="text" name="correo_empleado" placeholder="Correo">
        </div>
        <div class="form-group">
          <input type="text" name="Fecha_ing_empleado" placeholder="Fecha ingreso"
          onfocus="this.type='date'" onblur="if(!this.value) this.type='text'">
          <input type="text" name="salario_empleado" placeholder="Salario">
        </div>
        <div class="form-group">
          <input type="text" name="Estado_empleado" placeholder="Estado">
          <input type="text" name="nom_usuario" placeholder="Nombre de usuario">
        </div>
        <div class="form-group">
            <input type="text" name="contras" placeholder="Contaseña">
            <input type="text" name="id_rol_fk_empleado" placeholder="Identificador de rol">
        </div>
        <button type="submit" class="save-btn">Insertar</button>
      </form>
    </div>

    <div id="search" class="search"> 
        <form action="" method="get">
            <input type="text" name="search" placeholder="Escribe una palabara" id="searchInput">
            <input type="submit" value="Buscar" id="btnSearch">
        </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nombre</th>
          <th>Direccion</th>
          <th>Tipo de sangre</th>
          <th>Telefono</th>
          <th>Correo</th>
          <th>Fecha de ingreso</th>
          <th>Salario</th>
          <th>Estado</th>
          <th>Nombre de usuario</th>
          <th>Contraseña</th>
          <th>Numero de rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_empleado']; ?></td>
            <td><?php echo $row['nom_empleado']; ?></td>
            <td><?php echo $row['direccion_empleado']; ?></td>
            <td><?php echo $row['tipo_sangre']; ?></td>
            <td><?php echo $row['telefono_empleado']; ?></td>
            <td><?php echo $row['correo_empleado']; ?></td>
            <td><?php echo $row['Fecha_ing_empleado']; ?></td>
            <td><?php echo $row['salario_empleado']; ?></td>
            <td><?php echo $row['Estado_empleado']; ?></td>
            <td><?php echo $row['nom_usuario']; ?></td>
            <td><?php echo $row['contras']; ?></td>
            <td><?php echo $row['id_rol_fk_empleado']; ?></td>
            <td>
              <a class="btn" href="EDITAR_EMPLEADO.php?id_empleado=<?php echo $row['id_empleado']; ?>">Actualizar</a>
              <a class="btn" href="ELIMINAR_EMPLEADO.php?id_empleado=<?php echo $row['id_empleado']; ?>"
              onclick="return confirm('¿Deseas eliminar este rol?');">Eliminar</a>
            </td>
          </tr>
        <?php } ?>
        <?php } else { ?>
    <tr><td colspan="5">No se encontraron resultados</td></tr>
<?php } ?>
      </tbody>
    </table>
  </div>

  <!---------JAVA SCRIPT--------->
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      const toggleBtn = document.getElementById("formToggle");
      const submenu = document.getElementById("submenuForm");

      toggleBtn.addEventListener("click", function(e) {
        e.preventDefault();
        submenu.classList.toggle("show");
      });
    });
  </script>

</body>
</html>
