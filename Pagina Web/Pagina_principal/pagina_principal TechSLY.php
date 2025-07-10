<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Fashion Luxy</title>
  <link rel="stylesheet" type="text/css" href="/Pagina Web/CSS/index.css">
  <link rel="stylesheet" href="../bootstrap/css/bootstrap.min.css">
  <script src="../bootstrap/js/bootstrap.bundle.min.js"></script>
</head>
<body>
  <header id="header"></header>
  <br>
  <!--  -->
    <main>
      <section class="p-p">
        <div class="c-p">
          <img src="../IMG/Modelos 1.jpg" alt="Modelos" class="img-p">
          <div class="text">
            <h1 class="t-p">¡Pide</h1>
            <h2 class="t2-p">el tuyo!</h2>
            <button class="b-p">!Compra ya¡</button>
          </div>
        </div>
      </section>

      <br>
      <section class="seccion">
        <h2 class="titulo-seccion">Chaquetas</h2>
        <div class="contenedor-productos">
          <div class="producto">
            <img src="../IMG/Chaquet_de_cuero_hombre.jpeg" alt="Chaqueta cuero">
            <p>Chaqueta Black Panther</p>
          </div>
          <div class="producto">
            <img src="../IMG/chaqueta_clasica.jpeg" alt="Chaqueta clásica">
            <p>Chaqueta Clásica</p>
          </div>
          <div class="producto">
            <img src="../IMG/Chaqueta_moderna.jpeg" alt="Chaqueta moderna">
            <p>Chaqueta Moderna</p>
          </div>
        </div>
        <a href="#" class="ver-mas">Ver más productos</a>
      </section>
      <br>
      <section class="seccion">
        <h2 class="titulo-seccion">Pantalones</h2>
        <div class="contenedor-productos">
          <div class="producto">
            <img src="../IMG/cargo.jpeg" alt="Chaqueta cuero">
            <p>Chaqueta Black Panther</p>
          </div>
          <div class="producto">
            <img src="../IMG/Campana.jpeg" alt="Chaqueta clásica">
            <p>Chaqueta Clásica</p>
          </div>
          <div class="producto">
            <img src="../IMG/Baggy.jpeg" alt="Chaqueta moderna">
            <p>Chaqueta Moderna</p>
          </div>
        </div>
        <a href="#" class="ver-mas">Ver más productos</a>
      </section>
      <button class="ver-mas-final">Ver más</button>
      <hr>
      <br>
      <section>
        <div id="carruselAuto" class="carousel slide" data-bs-ride="carousel">

        <!-- Indicadores -->
        <div class="carousel-indicators">
          <button type="button" data-bs-target="#carruselAuto" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
          <button type="button" data-bs-target="#carruselAuto" data-bs-slide-to="1" aria-label="Slide 2"></button>
          <button type="button" data-bs-target="#carruselAuto" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>

        <!-- Imagenes -->
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img src="../IMG/Ropa modelaje 1.webp" style="with:60%; height: 30%;" class="d-block w-100" alt="Imagen 1">
          </div>
          <div class="carousel-item">
            <img src="../IMG/v-ropa.jpg" style="with:60%; height: 30%;" class="d-block w-100" alt="Imagen 2">
          </div>
          <div class="carousel-item">
            <img src="../IMG/Ropa modelaje.webp" style="with:60%; height: 30%;" class="d-block w-100" alt="Imagen 3">
          </div>
        </div>

        <!-- Controles -->
        <button class="carousel-control-prev" type="button" data-bs-target="#carruselAuto" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Anterior</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carruselAuto" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Siguiente</span>
        </button>
      </div>

      </section>
  </main>
  <br>
  <footer id="footer"></footer>

  <script> 
    fetch("header.php").then(res => res.text()) 
    .then(data => { document.getElementById("header").innerHTML = data; }); 

    function toggleSidebar() {
      document.getElementById('sidebar').classList.toggle('show');
    }

    fetch("footer.php") .then(res => res.text()) 
    .then(footer => { document.getElementById("footer").innerHTML = footer; }); 
  </script>

</body>
</html>
