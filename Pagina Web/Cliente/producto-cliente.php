<?php 
require_once "../PHP/CONFIG.php"; 
require_once "clase_cliente.php";  

$datos = [];
$obj = new PEDIDO();
    
$search=(isset($_GET['search'])) ? $_GET['search'] : "";
    $datos = $obj->CONSULTAR_PEDIDO($search); 
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../CSS/cliente.css">
    <title>Document</title>
</head>
<body>
    <header id="header-productocliente"></header>
    <div class="con-pro-cli">
        <div class="imgs-of-produc">
            <img src="../IMG/camisa_hombro.jpeg" class="imgs-of-produc" alt="hji">
            <img src="../IMG/camisa_hombro.jpeg" class="imgs-of-produc" alt="s">
            <img src="../IMG/camisa_hombro.jpeg" class="imgs-of-produc" alt="si">
        </div>
        <div class="img-prin-pro">
            <img src="../IMG/camisa_hombro.jpeg" class="img" alt="Producto">
        </div>
        <div class="form-pro">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
              <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
            </svg>
            <form action="insertar_cliente.php" method="post">
                <pre class="readonly"><input type="text" class="nombre" name="nomPedido" value="BLUSA HOMBRO DESCUBIERTO" readonly style="font-size: 25px; width: 70%; font-family:Georgia, 'Times New Roman', Times, serif;"></pre>
                <div>
                    <!--Material-->
                    <label for="categoria" class="subinfo" style="font-family: Georgia, 'Times New Roman', Times, serif;"">Material:</label>
                    <pre class="readonly"><input type="text" class="categoria" name="material" value="Algodon" readonly style="margin: 6px ; font-family: Georgia, 'Times New Roman', Times, serif;"></pre>
                </div>
                <br>
                <!--el valor-->
                <label for="valor" class="subinfo" style="font-family: Georgia, 'Times New Roman', Times, serif;">Valor:</label>
                <pre class="readonly">$<input type="text"  class="valor" name="valor" value="45.000" readonly style="font-family: Georgia, 'Times New Roman', Times, serif;"></pre>
                <br>
                <!--Tala-->
                <label for="talla" class="sec-for-pro subinfo" style="font-family: Georgia, 'Times New Roman', Times, serif;">Talla:</label>
                
                <input type="radio" name="talla" id="talla-s" value="S">
                <label for="talla-s" class="btn-talla">S</label>
                    
                <input type="radio" name="talla" id="talla-m" value="M">
                <label for="talla-m" class="btn-talla">M</label>
                    
                <input type="radio" name="talla" id="talla-l" value="L">
                <label for="talla-l" class="btn-talla">L</label>
                        
                <input type="radio" name="talla" id="talla-xl" value="XL">
                <label for="talla-xl" class="btn-talla">XL</label>
                    
                <input type="radio" name="talla" id="talla-xxl" value="XXL">
                <label for="talla-xxl" class="btn-talla">XXL</label>
                <br><br>
                <div class="color-picker subinfo">
                    <!-- aqui esta  los colores -->
                    <p class="sec-for-pro" style="font-family: Georgia, 'Times New Roman', Times, serif;">Elige un color:</p>

                    <input type="radio" name="color" id="color-rojo" value="Rojo">
                    <label for="color-rojo" class="color-option rojo"></label>

                    <input type="radio" name="color" id="color-azul" value="Azul">
                    <label for="color-azul" class="color-option azul"></label>

                    <input type="radio" name="color" id="color-blanco" value="Blanco">
                    <label for="color-blanco" class="color-option blanco"></label>

                    <input type="radio" name="color" id="color-negro" value="Negro">
                    <label for="color-negro" class="color-option negro"></label>
                </div>
                <div>
                    <!--categoria-->
                    <label for="categoria" class="subinfo">Categoria:</label>
                    <pre class="readonly"><input type="text" class="categoria "name="categoria" value="Blusa" readonly></pre>
                    <br><br>
                    <label for="cantidad" class="subinfo">Cantidad:</label>
                    <input type="text" name="cantidad" id="cantidad">
                </div>

                <br>
                <button type="button" class="btn" id="add-car-shop">Comprar</button>
                <br>
                <div class="descripcion-container">
                    <div class="descripcion-header">
                        <label for="descrip" class="titulo-desc">Descripción</label>
                        <span class="arrow-desc">▶</span>
                    </div>
                    <input type=""  readonly id="descrip-produc" name="descipcion" class="hidden" value="camisa de algodon ajustada al cuerpo">
                </div>
            </form>
            <br>


        </div>
    </div>
    <br>
    <hr>
    <br>
    <div>
    </div>
    <script src="../JS/clien.js">
        
    </script>
</body>
</html>