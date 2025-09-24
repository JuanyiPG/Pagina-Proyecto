<?php 
require_once "CONEXION.php"; 
require_once "CLASE_MATERIAP.php";  

$datos = [];
$obj = new MATERIA_P();
    
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $datos = $obj->Consultarmateriap_tPorID($search); 
} else {
    $datos = $obj->CONSULTAR_MATERIA_P(); 
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Materia prima</title>
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
      <h1>Gestión de Materia prima</h1>

     
      <form action="INSERTAR_MATERIAP.php" method="post">
        <div class="form-group">
          <input type="text" name="id_materia_p" placeholder="Código" required>
          <input type="text" name="nom_materia_p" placeholder="Nombre" required>
        </div>
        <div class="form-group">
          <input type="text" name="color_materia_p" placeholder="Color">
             <input type="text" name="categoria_mp" placeholder="Categoria">
        </div>
        <div class="form-group">
          <input type="text" name="tipo_material_materia_p" placeholder="Tipo de material">
        </div>
        <div class="form-group">
          <input type="text" name="stock_actual_materia_p" placeholder="Stock actual">
          <input type="text" name="stock_minimo_materia_p" placeholder="Stock minimo">
        </div>
        <div class="form-group">
          <input type="text" name="descripcion_materia_p" placeholder="Descripcion">
        </div>
        <div class="form-group">
          <input type="text" name="estado_materia_p" placeholder="Estado">
        </div>
        <button type="submit" class="save-btn">Insertar</button>
      </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>Código</th>
          <th>Nombre</th>
          <th>Color</th>
          <th>Categoria</th>
          <th>Tipo de material</th>
          <th>Stock actual</th>
          <th>Stock minimo</th>
          <th>descripcion</th>
          <th>estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
                  <div id="results" class="results">
        <?php 
        require_once '../conexion_b.php'; 
        $consulta="SELECT * FROM materia_prima";
        $filter = "";
        $search = (isset($_GET['search'])) ? $_GET['search'] : "";
        if(isset($search) && strlen($search)>3){
            $filter = " WHERE nom_materia_p LIKE '%$search%'"
                        or "WHERE id_materia_p LIKE '%$search%'";
            $consulta = $consulta . $filter; 
        }
        $results = mysqli_query($conn,$consulta);
        while($row = mysqli_fetch_array($results)){
        ?>
        <?php foreach ($datos as $row) { ?>
          <tr>
            <td><?php echo $row['id_materia_p']; ?></td>
            <td><?php echo $row['nom_materia_p']; ?></td>
            <td><?php echo $row['color_materia_p']; ?></td>
            <td><?php echo $row['categoria_mp']; ?></td>
            <td><?php echo $row['tipo_material_materia_p']; ?></td>
            <td><?php echo $row['stock_actual_materia_p']; ?></td>
            <td><?php echo $row['stock_minimo_materia_p']; ?></td>
            <td><?php echo $row['descripcion_materia_p']; ?></td>
            <td><?php echo $row['estado_materia_p']; ?></td>
            <td>
              <a class="btn-accion" href="EDITAR_MATERIAP.php?id_materia_p=<?php echo $row['id_materia_p']; ?>">Actualizar</a>
              <a class="btn-accion" href="ELIMINAR_MATERIAP.php?id_materia_p=<?php echo $row['id_materia_p']; ?>">Eliminar</a>
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
