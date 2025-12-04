<?php 
require_once "../PEDIDOS_EMPLE/CONEXION.PHP"; 
require_once "../PEDIDOS_EMPLE/CLASE_PEDIDOS_E.PHP";  
require_once "../../Items/header_emple.html";

$datos = [];
$obj = new PEDIDO();
    
$search = (isset($_GET['search'])) ? $_GET['search']: "";
    $datos = $obj->CONSULTAR_PEDIDO($search); 
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fctura Venta</title>
  <link rel="stylesheet" href="../../CSS/index.css">
</head>
<body class="body2">

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

  <div id="notificacion" style="
  position: fixed;
  top: 20px; right: 20px;
  background: #4caf50;
  color: white;
  padding: 15px;
  border-radius: 10px;
  display: none;
">
  📢 Nuevo pedido registrado
</div>
    <div class="cards">
      <h1>Tabla Pedidos</h1>
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
          <th>Enviar</th>
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
            <button class="btn-accion enviar-btn"  data-id="<?php echo $row['id_pedido']; ?>"
            data-nombre="<?php echo $row['nom_p_edido']; ?>"
            data-talla="<?php echo $row['talla_p_pedido']; ?>"
            data-color="<?php echo $row['color_p_pedido']; ?>"
            data-categoria="<?php echo $row['categoria_p_pedido']; ?>"
            data-material="<?php echo $row['material_p_pedido']; ?>"
            data-cantidad="<?php echo $row['cant_producto']; ?>"
            data-descripcion="<?php echo $row['descripcion_p_pedido']; ?>"
            data-fecha="<?php echo $row['fecha_pedido']; ?>"
            data-subtotal="<?php echo $row['sub_total_pedido']; ?>"
            data-valor="<?php echo $row['valor_pedido']; ?>"
            data-estado="<?php echo $row['estado_pedido']; ?>"
            data-cliente="<?php echo $row['id_cliente_fk_pedido']; ?>">Enviar a produccion</button>
            </td>
          </tr>
        <?php } ?>
        <?php } else { ?>
        <tr><td colspan="5">No se encontraron resultados</td></tr>
<?php } ?>
      </tbody>
    </table>
  </div>
  <script>
document.addEventListener("DOMContentLoaded", () => {
  const botones = document.querySelectorAll(".enviar-btn");

  botones.forEach(boton => {
    boton.addEventListener("click", async (e) => {
      e.preventDefault();

      const idPedido   = boton.getAttribute("data-id");
      const nombre     = boton.getAttribute("data-nombre");
      const talla      = boton.getAttribute("data-talla");
      const color      = boton.getAttribute("data-color");
      const categoria  = boton.getAttribute("data-categoria");
      const material   = boton.getAttribute("data-material");
      const cantidad   = boton.getAttribute("data-cantidad");
      const descripcion= boton.getAttribute("data-descripcion");
      const fecha      = boton.getAttribute("data-fecha");
      const subtotal   = boton.getAttribute("data-subtotal");
      const valor      = boton.getAttribute("data-valor");
      const estado     = boton.getAttribute("data-estado");
      const cliente    = boton.getAttribute("data-cliente");

      if (!idPedido) return;

      // Construcción correcta del body
      const body = 
        `id_pedido=${encodeURIComponent(idPedido)}&` +
        `nombre=${encodeURIComponent(nombre)}&` +
        `talla=${encodeURIComponent(talla)}&` +
        `color=${encodeURIComponent(color)}&` +
        `categoria=${encodeURIComponent(categoria)}&` +
        `material=${encodeURIComponent(material)}&` +
        `cantidad=${encodeURIComponent(cantidad)}&` +
        `descripcion=${encodeURIComponent(descripcion)}&` +
        `fecha=${encodeURIComponent(fecha)}&` +
        `subtotal=${encodeURIComponent(subtotal)}&` +
        `valor=${encodeURIComponent(valor)}&` +
        `estado=${encodeURIComponent(estado)}&` +
        `cliente=${encodeURIComponent(cliente)}`;

      try {
        const respuesta = await fetch("../../PHP/NOTIFICACIONES/enviar_a_produccion.php", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: body
        });

        const texto = await respuesta.text();
        console.log("📩 Respuesta cruda del servidor:", texto);

        let data;
        try {
          data = JSON.parse(texto);
        } catch (e) {
          throw new Error("El servidor no devolvió JSON válido");
        }

        if (data.success) {
          alert("✅ Pedido enviado a producción correctamente.");
          boton.disabled = true;
          boton.innerText = "Enviado";
        } else {
          alert("❌ Error: " + data.message);
        }
      } catch (err) {
        console.error("Error en la petición:", err);
        alert("⚠️ No se pudo conectar con el servidor.");
      }
    });
  });
});
</script>
<script>
function mostrarNotificacion(mensaje) {
  let notif = document.getElementById("notificacion");
  notif.textContent = mensaje;
  notif.style.display = "block";
  
  setTimeout(() => { notif.style.display = "none"; }, 3000); // se oculta en 3s
}

document.querySelector("form").addEventListener("submit", async function(e) {
  e.preventDefault();
  let datos = new FormData(this);

  let resp = await fetch("../Cliente/insertar_cliente.php", { method: "POST", body: datos });
  let text = await resp.text();

  if (text === "ok") {
    mostrarNotificacion("✅ Se registró un nuevo pedido");
  } else {
    mostrarNotificacion("❌ Error al guardar");
  }
});
</script>



</body>
</html>
