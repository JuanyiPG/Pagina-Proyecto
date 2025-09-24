<?php 
require_once "CONEXION.php"; 
require_once "CLASE_PRODUCTO_T.php";  

$datos = [];
$obj = new PRODUCTO_T();
    
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $datos = $obj->ConsultarProducto_tPorID($search); 
} else {
    $datos = $obj->CONSULTAR_PRODUCTO_T(); 
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Producto terminado</title>
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
      <h1>Gestión de productos</h1>

     
      <form action="INSERTAR.php" method="post">
        <div class="form-group">
          <input type="text" name="id_producto_t" placeholder="Código" required>
          <input type="text" name="nombre_producto_t" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="descripcion_producto_t" placeholder="Descripcion">
        </div>
        <div class="form-group">
          <input type="text" name="categoria_produ_t" placeholder="Categoria">
        </div>
        <div class="form-group">
          <input type="text" name="unidad_medida" placeholder="Medida">
          <input type="text" name="estado_producto_t" placeholder="Estado">
        </div>
        <div class="form-group">
          <input type="text" name="id_produccion_fk_producto_terminado" placeholder="Identificador de el el numero de produccion">
        </div>
        <button type="submit" class="save-btn">Insertar</button>
      </form>
    </div>
      <div id="search" class="search"> 
        <form action="index_b.php">
            <input type="text" name="search" placeholder="Escribe una palabara">
            <input type="submit" value="Buscar">
        </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nombre</th>
          <th>Descripcion</th>
          <th>Categoria</th>
          <th>Unidad de medida</th>
          <th>Estado</th>
          <th>Identificador</th>
          <th>Acciones</th>
        </tr>
      </thead>
          <div id="results" class="results">
        <?php 
        require_once '../conexion_b.php'; 
        $consulta="SELECT * FROM producto_terminado";
        $filter = "";
        $search = (isset($_GET['search'])) ? $_GET['search'] : "";
        if(isset($search) && strlen($search)>3){
            $filter = " WHERE nombre_producto_t LIKE '%$search%'"
                        or "WHERE categoria_produ_t LIKE '%$search%'";
            $consulta = $consulta . $filter; 
        }
        $results = mysqli_query($conn,$consulta);
        while($row = mysqli_fetch_array($results)){
        ?>
      <tbody>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_producto_t']; ?></td>
            <td><?php echo $row['nombre_producto_t']; ?></td>
            <td><?php echo $row['descripcion_producto_t']; ?></td>
            <td><?php echo $row['categoria_produ_t']; ?></td>
            <td><?php echo $row['unidad_medida']; ?></td>
            <td><?php echo $row['estado_producto_t']; ?></td>
            <td><?php echo $row['id_produccion_fk_producto_terminado']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_PRODUCTOT.php?id_producto_t=<?php echo $row['id_producto_t']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_PRODUCTOT.php?id_producto_t=<?php echo $row['id_producto_t']; ?>">Eliminar</a>
            </td>
          </tr>
      </tbody>
    </table>
            <?php
        }
        ?>
  </div>

</body>
</html>
<?php
        }
        ?>
