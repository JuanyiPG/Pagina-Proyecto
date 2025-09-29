<?php
header("Content-Type: text/html; charset=UTF-8");

$file = __DIR__ . "/produccion.json";
$pedidos = [];

if (file_exists($file)) {
    $json = file_get_contents($file);
    $pedidos = json_decode($json, true) ?? [];
}
?>

<?php
require_once "../../Items/header-admin.html"
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Producción</title>
    <link rel="stylesheet" href="../../CSS/index.css">
    <style>
    </style>
</head>
<body class="body2">
    <div class="cardo">
        <h2>PEDIDOS PARA PRODUCCION</h2>
        <?php if (empty($pedidos)): ?>
            <p style="text-align:center;">No hay pedidos enviados todavía.</p>
        <?php else: ?>
        <table class="tables">
            <thead class="theads">
                <tr>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Talla</th>
                    <th>Color</th>
                    <th>Categoría</th>
                    <th>Material</th>
                    <th>Cantidad</th>
                    <th>Descripción</th>
                    <th>Fecha</th>
                    <th>Subtotal</th>
                    <th>Valor</th>
                    <th>Estado</th>
                    <th>Cliente</th>
                </tr>
            </thead>
            <tbody class="tbodys">
                <?php foreach ($pedidos as $p): ?>
                    <tr>
                        <td class='articulos'><?= $p['id_pedido'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['nombre'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['talla'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['color'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['categoria'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['material'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['cantidad'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['descripcion'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['fecha'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['subtotal'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['valor'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['estado'] ?? '-' ?></td>
                        <td class='articulos'><?= $p['cliente'] ?? '-' ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>
    </div>

<!-------------JAVA SCRIPT ----------------->
<!-------------header---------------->
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
