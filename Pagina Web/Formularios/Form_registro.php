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
      background-color: beige;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .nav {
      background-color: #ca7575;
      width: 100%;
      position: fixed;
      top: 0;
      left: 0;
      z-index: 1000;
    }

     .nav img{
      height: 40px;
      margin-top: 5px ;
      padding-top: 5px;
    }

    .nav ul li a i{
      border-radius: 5px;
      padding: 1px 20px;
      width: 50px;
      height: 100px;
      color: #000
    }
    .nav ul li a i:hover{
      background-color: #834343;
      color: antiquewhite;
      border-radius: 5px;
      padding: 1px 20px;
      width: 50px;
      height: 100%;
    }

    .nav ul li a i{
      font-size: 40px;
    }

    form {
      background-color: whitesmoke;
      padding: 40px;
      border-radius: 20px;
      width: 400px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
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
      background-color: #ca7575;
      border-radius: 20px;
      border: 1px solid #834343;
      width: 100%;
      padding: 10px;
      margin-top: 20px;
      cursor: pointer;
    }

    form button p {
      color: whitesmoke;
      margin: 0;
      text-align: center;
    }

    form button:hover{
      background-color: rgb(129, 30, 30);
      background-color: #834343;
      box-shadow: -2px 5px 1px 2px #000 ;
      margin-left: -3px;
    }

  </style>
</head>
<body>

  <div class="nav">
    <ul>
      <li class="m-left" id="list"><a href="/Pagina_principal/pagina_principal TechSLY.html"><i class="bi bi-house-door-fill"></i></a>
      <img src="/IMG/logo rosa.jpeg" alt="Logo">
      </li>
    </ul>
  </div>

  <form action="">
    <h1>Registro</h1>
    <hr>
    <label for="name">Nombre</label>
    <input type="text" pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+" title="Solo se permiten letras A-Z, a-z" required>

    <label for="second_name">Apellido</label>
    <input type="text" pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+" title="Solo se permiten letras A-Z, a-z" required>

    <label for="correo">Correo</label>
    <input type="email" name="correo" required>

    <label for="date">Fecha de nacimiento</label>
    <input type="date" name="datemind" id="datemind" min="2007-01-01" required>

    <label for="username" >Nombre de usuario</label>
    <input type="text" required>

    <label for="password">Contraseña</label>
    <input type="password" required>
    <br><br>
    <a href="/Formularios/form.html">¿Ya tiene una cuenta?</a>
    <br><br>
    <button><p>Registrarse</p></button>

  </form>

</body>
</html>
