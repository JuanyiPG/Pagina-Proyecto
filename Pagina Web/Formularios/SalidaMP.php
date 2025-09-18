<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Materia Prima</title>
    <link rel="stylesheet" href="/Pagina Web/CSS/materia-prima.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet">
    <script rel="stylesheet" src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
    <header id="header-admin"></header>
    <div class="main">
        <div class="card">
            <h1 class="login__title"> SALIDA MATERIA PRIMA </h1>

            <form>
            <div class="form-group">
                <div class="Fecha">
                        <div class="login__box-input">
                            <label for="" class="login__label" >Fecha de salida</label>
                            <input type="date" name="Fecha" id="" required>
                        </div>
                </div>

            <div class="form-group">
                <label for="" class="login__label">Categoria</label>
                <select name="Cat" id="Cat" required >
                    <option value="" disabled selected hidden></option>
                    <option value="Hilo">Hilo</option>
                    <option value="Guata">Guata</option>
                    <option value="Tela">Tela</option>
                    <option value="Insumos">Insumos</option>
                </select>
            </div>

                <div class="form-group">

                    <div class="login__box-input" id="campoMaterial">
                        <label for="" class="login__label">Nombre del material</label>
                        <input type="text" name="material" id="material" required>
                        <i class="ri-eye-off-lie login_eye"></i>
                    </div>
                </div>

                    <div class="form-group">

                    <div class="login__box-input" id="campoInsumos">
                        <label for="" class="login__label">Descripción de los insumos</label>
                        <input type="text" name="material" id="material" required>
                        <i class="ri-eye-off-lie login_eye"></i>
                    </div>
                </div>

                <div class="form-group"></div>
                        <label for="" class="login__label">Color</label>
                        <input type="text" name="Color" id="" required>
                        <i class="ri-eye-off-lie login_eye"></i>
                </div>

            
                    <div class="form-group">
                        <label for="" class="login__label">Unidad de medida</label>
                        <select name="UniMed" id="" required>
                    <option value="" disabled selected hidden></option>
                    <option value="Metros">Metros</option>
                    <option value="Kilos">Kilos</option>
                    <option value="Unidad">Unidad</option>
                </select>
                    </div>

                    <div class="form-group">
                        <label for="" class="login__label">Cantidad</label>
                        <input type="number" name="Cant" id="" required>
                    </div>

                    <div class="form-group">
                        <label for="" class="login__label">Precio unitario</label>
                        <input type="text" name="" id="">
                        <i class="ri-eye-off-lie login_eye"></i>
                    </div>

                <div class="form-group">
            <div class="login__box-input" id="campoDestino">
                <label for="" class="login__label">Destino</label>
                <select name="Destino" id="Destino" required >
                    <option value="" disabled selected hidden></option>
                    <option value="Corte">Corte</option>
                    <option value="Tinturado">Tinturado</option>
                    <option value="Taller">Taller</option>
                </select>
            </div>
            </div>

            <div class="form-group">
                        <div class="login__box-input" id="campoDestino2">
                <label for="" class="login__label">Destino 2</label>
                <select name="Destino2" id="Destino2" required >
                    <option value="" disabled selected hidden></option>
                    <option value="Taller">Taller</option>
                    <option value="Bordado">Bordado</option>
                    <option value="Estampado">Estampado</option>
                </select>
            </div>

            <div class="form-group">
                    <div class="login__box-input" id="campoNT">
                        <label for="" class="login__label">Nombre del Taller</label>
                        <input type="text" name="campoNT" id="campoNT" required>
                    </div>
                </div>

            <button type="submit" class="btn-accion">Registrar</button>
        </form>
    </div>
    </div>
    <script>
    //Selecciona el id Cat
const cat = document.getElementById("Cat");
cat.addEventListener("change", () => {
    //oculta los campos 
    document.getElementById("campoMaterial").classList.add("hidden");
    document.getElementById("campoInsumos").classList.add("hidden");

    const seleccionados = Array.from(cat.selectedOptions).map(opt => opt.value);
//muestra el campo segun seleccione
    if (seleccionados.includes("Tela")) {
    document.getElementById("campoMaterial").classList.remove("hidden");
    }
    if (seleccionados.includes("Insumos")) {
    document.getElementById("campoInsumos").classList.remove("hidden");
    }
    
});

// Selecciona el id "Destino"
const destino = document.getElementById("Destino");
destino.addEventListener("change", () => {
        //oculta los campos 
    document.getElementById("campoDestino2").classList.add("hidden");
    document.getElementById("campoNT").classList.add("hidden");
//muestra el campo segun seleccione
const seleccionados = Array.from(destino.selectedOptions).map(opt => opt.value);
        if (seleccionados.includes("Corte")) {
    document.getElementById("campoDestino2").classList.remove("hidden");
        }

    if (seleccionados.includes("Taller")) {
    document.getElementById("campoNT").classList.remove("hidden");
    }
    
});

const destino2 = document.getElementById("Destino2");
destino2.addEventListener("change", () => {
        //oculta los campos 
    document.getElementById("campoNT").classList.add("hidden");
//muestra el campo segun seleccione
const seleccionados = Array.from(destino2.selectedOptions).map(opt => opt.value);

    if (seleccionados.includes("Taller")) {
    document.getElementById("campoNT").classList.remove("hidden");
    }
    
});

    const cantidad = document.getElementById("cantidad");
    const precio = document.getElementById("precio");
    const total = document.getElementById("total");

    function calcularTotal() {
    const cant = parseFloat(cantidad.value) || 0;
    const prec = parseFloat(precio.value) || 0;
      total.value = (cant * prec).toFixed(2);
    }

    // Escuchar cambios en los campos
    cantidad.addEventListener("input", calcularTotal);
    precio.addEventListener("input", calcularTotal);
</script>

</body>
</html>

<?php
require_once 'MateriaPrimap.php'; 
?>