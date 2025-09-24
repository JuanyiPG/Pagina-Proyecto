<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles_b.css">
    <title>Buscador con php</title>
</head>
<body>
    <div id="search" class="search"> 
        <form action="index_b.php">
            <input type="text" name="search" placeholder="Escribe una palabara" id="searchInput">
            <input type="submit" value="Buscar" id="btnSearch">
        </form>
    </div>
    <div id="results" class="results">
        <?php 
        require_once 'conexion-b.php'; 
        $consulta="SELECT * FROM producto_terminado";
        $filter = "";
        $search = (isset($_GET['search'])) ? $_GET['search'] : "";
        if(isset($search) && strlen($search)>3){
            $filter = " WHERE estado LIKE '%$search%'";
            $consulta = $consulta . $filter; 
        }
        $results = mysqli_query($conn,$consulta);
        while($row = mysqli_fetch_array($results)){
        ?>
        <div class="items">
            <h2></h2>
            <h3></h3>
            <p></p>
        </div>
        <?php
        }
        ?>
    </div>
    <script src="../JS/index.js"></script>
</body>
</html>