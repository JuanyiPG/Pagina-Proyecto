<?php 
require_once "../CONFIG.php"; 
require_once "CLASE_PEDIDO.PHP";  

$datos = [];
$obj = new PEDIDO();
    
$search=(isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_PEDIDO($search); 
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pedido</title>
  <link rel="stylesheet" href="../../CSS/index.css">
  <body class="body2">


  <div class="main">
    <div class="card">
      <h1>Gestión de pedidos</h1>

     
      <form action="INSERTAR_PEDIDO.PHP" method="post">
        <div class="form-group">
          <input type="text" name="id_pedido" placeholder="Numero de pedido" required>
          <input type="text" name="nom_p_edido" placeholder="Nombre " required>
        </div>
        <div class="form-group">
          <input type="text" name="talla_p_pedido" placeholder=" talla"required>
          <input type="text" name="color_p_pedido" placeholder="Color"required>
        </div>
        <div class="form-group">
          <input type="text" name="categoria_p_pedido" placeholder="Categoria"required>
          <input type="text" name="material_p_pedido" placeholder="Material"required>
        </div>
        <div class="form-group">
          <input type="text" name="cant_producto" placeholder="Cantidad"required>
          <input type="text" name="descripcion_p_pedido" placeholder="descripcion"required>
        </div>
        <div class="form-group">
          <input type="text" name="fecha_pedido" = "text" placeholder="fecha de pedido" required
          onfocus="this.type='date'" onblur="if(!this.value) this.type='text'">
          <input type="text" name="sub_total_pedido" placeholder="sub total"required>
        </div>
         <div class="form-group">
          <input type="text" name="valor_pedido" placeholder="Valor"required>
          <input type="text" name="estado_pedido" placeholder="estado"required>
        </div>
         <div class="form-group">
          <input type="text" name="id_cliente_fk_pedido" placeholder="numero de cliente que hizo el pedido"required>
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
          <th>nombre</th>
          <th>talla</th>
          <th>Color</th>
          <th>Categoria</th>
          <th>Material</th>
          <th>Cantidad de producto</th>
          <th>descripcion</th>
          <th>fecha de el pedido</th>
          <th>sub total</th>
          <th>valor</th>
          <th>estado</th>
          <th>numero de cliente que realizo el pedido</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!empty($datos)) { ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_pedido']; ?></td>
            <td><?php echo $row['nom_p_edido']; ?></td>
            <td><?php echo $row['talla_p_pedido']; ?></td>
            <td><?php echo $row['color_p_pedido']; ?></td>
            <td><?php echo $row['categoria_p_pedido']; ?></td>
            <td><?php echo $row['material_p_pedido']; ?></td>
            <td><?php echo $row['cant_producto']; ?></td>
            <td><?php echo $row['descripcion_p_pedido']; ?></td>
            <td><?php echo $row['fecha_pedido']; ?></td>
            <td><?php echo $row['sub_total_pedido']; ?></td>
            <td><?php echo $row['valor_pedido']; ?></td>
            <td><?php echo $row['estado_pedido']; ?></td>
            <td><?php echo $row['id_cliente_fk_pedido']; ?></td>
            <td>
              <a class="btn" href="EDITAR_PEDIDO.php?id_pedido=<?php echo $row['id_pedido']; ?>">Actualizar</a>
              <a class="btn" href="ELIMINAR_PEDIDO.php?id_pedido=<?php echo $row['id_pedido']; ?>"
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
<!---JAVA SCRIPT------>
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
