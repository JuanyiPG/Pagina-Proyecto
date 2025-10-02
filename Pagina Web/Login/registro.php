<?php
require_once "../PHP/CONFIG.PHP"; 
require_once "../Login/CLASE_REGISTRO.PHP";  

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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../Login/index.css">
    <title>Login</title>
    <style>
       *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body{
            height: 100vh;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .nav {
        background: linear-gradient(to right, rgb(255, 255, 255), #5c0b26);
        display: flex;
        width: 100%;
        position: fixed;
        align-items: center;
        top: 0;
        left: 0;
        z-index: 1000;
        }

        .nav img{
        height: 100%;
        width: 140px;
        margin-top: 0px ;
        padding-top: 0px;
        }

        .nav ul {
        padding: 1px 20px;
        }

        .nav ul{
        display: flex;
        }

  </style>
</head>
<body>

<div class="nav">
    <ul>
      <a href="../../index.html"> 
        <img src="../IMG/Logo_Luxy_Fashion.png" alt="Logo">
      </a>
    </ul>
  </div>
    <div class="container-l">
        <div class="container-l-f">
            <form action class="sign-in">
         <?php if (isset($_GET['mensaje'])): ?>
             <?php if ($_GET['mensaje'] == "ok"): ?>
                <div style= "color: green">
                   <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16">
                      <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                    </svg> 
                </div>
            <?php else: ?>
            <div style="color: red; text-align:center; margin: 10px;">
               ❌ Error al registrar cliente
            </div>
         <?php endif; ?>
   <?php endif; ?>
                <h2>Iniciar sesión</h2>
                <span>Use su email y contraseña</span>
                <div class="container-input">
                    <input type="email" placeholder="Email" required>
                </div>
                <div class="container-input">
                    <input type="password" placeholder="Contraseña" required>
                </div>
                <a href="#">¿Olvidaste tu contraseña?</a>
                <button type="submit" class="button-ingre">Ingresar</button>
            </form>
        </div>
        <div class="container-l-f">
            <form form action="../Login/INSERT_REGISTRO.PHP" method="post"class="sign-up">
                <h2>Registrarse</h2>
                <span>realize el formulario</span>
                <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-person-fill" viewBox="0 0 16 16">
                        <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0m2 5.755V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-.245S4 12 8 12s5 1.755 5 1.755"/>
                    </svg>
                    <input type="text" name= "id_cliente" placeholder="Cedula" required>
                </div>
                <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-person-fill" viewBox="0 0 16 16">
                        <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0m2 5.755V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-.245S4 12 8 12s5 1.755 5 1.755"/>
                    </svg>
                    <input type="text" name ="nom_cliente" placeholder="Nombre Completo" required>
                </div>
                <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-badge" viewBox="0 0 16 16">
                        <path d="M6.5 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                        <path d="M4.5 0A2.5 2.5 0 0 0 2 2.5V14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2.5A2.5 2.5 0 0 0 11.5 0zM3 2.5A1.5 1.5 0 0 1 4.5 1h7A1.5 1.5 0 0 1 13 2.5v10.795a4.2 4.2 0 0 0-.776-.492C11.392 12.387 10.063 12 8 12s-3.392.387-4.224.803a4.2 4.2 0 0 0-.776.492z"/>
                    </svg>
                    <input type="text" name= "direccion_cliente" placeholder="direccion" required>
                </div>
                <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telephone" viewBox="0 0 16 16">
                      <path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.6 17.6 0 0 0 4.168 6.608 17.6 17.6 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.68.68 0 0 0-.58-.122l-2.19.547a1.75 1.75 0 0 1-1.657-.459L5.482 8.062a1.75 1.75 0 0 1-.46-1.657l.548-2.19a.68.68 0 0 0-.122-.58zM1.884.511a1.745 1.745 0 0 1 2.612.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z"/>
                    </svg>
                    <input type="text" name= "telefono_cliente" placeholder="telefono cliente" required>
                </div>
                 <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-at" viewBox="0 0 16 16">
                       <path d="M2 2a2 2 0 0 0-2 2v8.01A2 2 0 0 0 2 14h5.5a.5.5 0 0 0 0-1H2a1 1 0 0 1-.966-.741l5.64-3.471L8 9.583l7-4.2V8.5a.5.5 0 0 0 1 0V4a2 2 0 0 0-2-2zm3.708 6.208L1 11.105V5.383zM1 4.217V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v.217l-7 4.2z"/>
                       <path d="M14.247 14.269c1.01 0 1.587-.857 1.587-2.025v-.21C15.834 10.43 14.64 9 12.52 9h-.035C10.42 9 9 10.36 9 12.432v.214C9 14.82 10.438 16 12.358 16h.044c.594 0 1.018-.074 1.237-.175v-.73c-.245.11-.673.18-1.18.18h-.044c-1.334 0-2.571-.788-2.571-2.655v-.157c0-1.657 1.058-2.724 2.64-2.724h.04c1.535 0 2.484 1.05 2.484 2.326v.118c0 .975-.324 1.39-.639 1.39-.232 0-.41-.148-.41-.42v-2.19h-.906v.569h-.03c-.084-.298-.368-.63-.954-.63-.778 0-1.259.555-1.259 1.4v.528c0 .892.49 1.434 1.26 1.434.471 0 .896-.227 1.014-.643h.043c.118.42.617.648 1.12.648m-2.453-1.588v-.227c0-.546.227-.791.573-.791.297 0 .572.192.572.708v.367c0 .573-.253.744-.564.744-.354 0-.581-.215-.581-.8Z"/>
                     </svg>
                    <input type="text" name = "correo_cliente" placeholder="Correo" required>
                </div>
                <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-badge" viewBox="0 0 16 16">
                         <path d="M6.5 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                         <path d="M4.5 0A2.5 2.5 0 0 0 2 2.5V14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2.5A2.5 2.5 0 0 0 11.5 0zM3 2.5A1.5 1.5 0 0 1 4.5 1h7A1.5 1.5 0 0 1 13 2.5v10.795a4.2 4.2 0 0 0-.776-.492C11.392 12.387 10.063 12 8 12s-3.392.387-4.224.803a4.2 4.2 0 0 0-.776.492z"/>
                     </svg>
                    <input type="text" name = "nombre_usuari" placeholder="nombre de usuario" required>
                </div>
                 <div class="container-input">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-lock" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 0a4 4 0 0 1 4 4v2.05a2.5 2.5 0 0 1 2 2.45v5a2.5 2.5 0 0 1-2.5 2.5h-7A2.5 2.5 0 0 1 2 13.5v-5a2.5 2.5 0 0 1 2-2.45V4a4 4 0 0 1 4-4M4.5 7A1.5 1.5 0 0 0 3 8.5v5A1.5 1.5 0 0 0 4.5 15h7a1.5 1.5 0 0 0 1.5-1.5v-5A1.5 1.5 0 0 0 11.5 7zM8 1a3 3 0 0 0-3 3v2h6V4a3 3 0 0 0-3-3"/>
                    </svg>
                    <input type="password" name = "contra" placeholder="Contraseña" required>
                </div>
                <div class="">
                     <input type="hidden" name="id_rol_fk_cliente" value="3">
                </div>
                <button type="submit" class="button-ingre">Registrarse</button>
            </form>
        </div>
        <div class="container-w-l">
            <div class="container-l-sign-up welcome">
                <h3>Bienvenido</h3>
                <p>Ingrese sus datos personales para usar todas las funciones del sitio</p>
                <button class="button-login" id="btn-sign-up">Registrarse</button>
            </div>
            <div class="container-l-sign-in welcome">
                <h3>¡Hola!</h3>
                <p>Registrese con sus datos pesonales para usar todas las funciones del sitio</p>
                <button class="button-login" id="btn-sign-in">Iniciar Sesión</button>
            </div>
            
        </div>
    </div>
    
    <script src="../Login/login.js"></script>
    
</body>
</html>