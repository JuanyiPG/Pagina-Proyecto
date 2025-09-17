<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  
  <title>Registro</title>
  <style>
    * {
      padding: 0;
      margin: 0;
      box-sizing: border-box;
    }

    body {
      background-color: whitesmoke;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

     body {
      background-color: whitesmoke;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
      height: 90%;
      width: 120px;
      margin-top: 0px ;
      padding-top: 0px;
    }

    .nav ul {
      border-radius: 5px;
      padding: 1px 20px;
      width: 1000px;
      height: 80px;
      color: #000;
      font-size: 40px;
    }

    .nav ul{
      display: flex;
    }

    form {
      background-color: whitesmoke;
      padding: 40px;
      border-radius: 20px;
      width: 650px;
      box-shadow: 0 4px 10px rgba(82, 60, 60, 1);
      margin: 100px auto 40px auto;
    }

    form h1 {
      margin-bottom: 20px;
      text-align: center;
    }

    form label {
      display: block;
      margin-top: 15px;
      color: black;
    }

    form input {
      border: 1px solid #ccc;
      border-radius: 30px;
      margin-top: 5px;
      padding: 10px 15px;
      width: 100%;
      outline: none;
    }

    form input:focus {
      border-color: #834343;
    }

    form button {
      background-color:#5c0b26;
      border-radius: 20px;
      color:  white;
      border: 1px solid #834343;
      width: 100%;
      padding: 10px;
      margin-top: 20px;
      cursor: pointer;
    }

    form button a{
      color: whitesmoke;
      text-decoration: none;
      margin: 0;
      text-align: center;
    }


    form button:hover{
      background-color: #8d103a;
      box-shadow: -2px 1px 1px 1px #3d0518 ;
      margin-left: -3px;
    }

    .camps{
      display: flex;
      justify-content: space-between;
    }

    .colum-left, .colum-right {
      display: inline-block;
      width: 45%;
      vertical-align: top;
      margin: 0 5px;
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

  <form action="../Admin/index-admin.php">
    <h1>Registro</h1>
    <hr>
    <div clas="camps">

      <div class="colum-left">
        <label for="name">Nombre</label>
        <input type="text" pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+" title="Solo se permiten letras A-Z, a-z" required>
        
        <label for="second_name">Apellido</label>
        <input type="text" pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+" title="Solo se permiten letras A-Z, a-z" required>
        
        <label for="correo">Correo</label>
        <input type="email" name="correo" required>
      </div>
      <div class="colum-right">
        <label for="date">Fecha de nacimiento</label>
        <input type="date" name="datemind" id="datemind" min="2007-01-01" required>
        
        <label for="username" >Nombre de usuario</label>
        <input type="text" required>
        
        <label for="password">Contraseña</label>
        <input type="password" required>
      </div>
    </div>
      <br><br>
      <a href="Inicio-sesion.html">¿Ya tiene una cuenta?</a>
      <br><br>
    <button><p>Registrarse</p></button>

  </form>

</body>
</html>
