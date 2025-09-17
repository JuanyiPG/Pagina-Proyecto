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
  <style>
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body {
      display: flex;
      height: 100vh;
      background-color: #f5f6fa;
    }


    .menulateral {
      width: 250px;
      background: linear-gradient(180deg, white, #d1b7c2);
      color: rgb(104, 10, 41);
      padding: 20px 0;
      display: flex;
      flex-direction: column;
      border-right: 2px solid #ddd;
    }

    .menulateral .logo img {
      width: 180px;
      height: auto;
      margin: 0 auto;
      display: block;
    }

    .menulateral hr {
      margin: 15px 0;
      border: none;
      border-top: 1px solid rgba(255,255,255,0.3);
    }

    .menulateral ul {
      list-style: none;
      margin-top: 20px;
      font-weight: bold;
    }

    .menulateral ul li {
      padding: 12px 20px;
      cursor: pointer;
      transition: 0.3s;
      border-radius: 8px;
    }

    .menulateral ul li:hover,
    .menulateral ul li.active {
      background: rgb(104, 10, 41);
      color: white;
      font-weight: bold;
    }

    .main {
      flex: 1;
      padding: 30px;
      overflow-y: auto;
    }

    .main h2 {
      font-size: 24px;
      margin-bottom: 20px;
    }

    .card {
      background: #ffffff;
      padding: 40px;
      border-radius: 15px;
      max-width: 900px;
      margin: auto;
      margin-bottom: 40px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .card h1 {
      text-align: center;
      margin-bottom: 40px;
      color: rgb(104, 10, 41);
    }

    form .form-group {
      display: flex;
      gap: 20px;
      margin-bottom: 20px;
    }

    form .form-group input {
      flex: 1;
      padding: 12px;
      border-radius: 8px;
      border: 1px solid #ddd;
      outline: none;
      font-size: 14px;
    }

    form .form-group input:focus {
      border-color: rgb(104, 10, 41);
    }

    .save-btn {
      margin-top: 10px;
      background: rgb(104, 10, 41);
      color: #fff;
      padding: 12px 25px;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      font-size: 15px;
      font-weight: bold;
      transition: 0.3s;
      display: block;
      margin-left: auto;
      margin-right: auto;
    }

    .save-btn:hover {
      background: #8c1238;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
      background: #fff;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    table th, table td {
      padding: 12px;
      text-align: center;
      border-bottom: 1px solid #ddd;
    }

    table th {
      background: #5e0925;
      color: white;
      font-size: 14px;
    }

    table td {
      font-size: 14px;
    }

    .btn-accion {
      padding: 6px 12px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 13px;
      color: #fff;
      background-color: #5e0925;
      margin: 2px;
    }

    .btn-accion:hover {
      background-color: #8c1238;
    }
</style>
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
        <?php } ?>
      </tbody>
    </table>
  </div>

</body>
</html>
