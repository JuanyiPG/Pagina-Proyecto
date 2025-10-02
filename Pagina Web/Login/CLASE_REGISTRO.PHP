<?php

class CLIENTE
{
    public function INSERT_CLIENTE($datos_registro)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Cliente(?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("ississsi", 
            $datos_registro[0], 
            $datos_registro[1], 
            $datos_registro[2], 
            $datos_registro[3], 
            $datos_registro[4], 
            $datos_registro[5],
            $datos_registro[6],
            $datos_registro[7]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_CLIENTE()
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Cliente()";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $cliente = [];
        while ($row = $resultado->fetch_assoc()) {
            $cliente[] = $row;
        }

        $resultado->free();
        return $cliente; 
    }
}
?>