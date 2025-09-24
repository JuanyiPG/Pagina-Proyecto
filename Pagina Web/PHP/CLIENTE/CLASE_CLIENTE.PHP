<?php

class CLIENTE
{
    public function INSERT_CLIENTE($datos_cliente)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Cliente(?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("issisi", 
            $datos_cliente[0], 
            $datos_cliente[1], 
            $datos_cliente[2], 
            $datos_cliente[3], 
            $datos_cliente[4], 
            $datos_cliente[5]
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

    public function ACTUALIZAR_CLIENTE($datos_cliente)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Cliente(?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("issisi",
            $datos_cliente[0], 
            $datos_cliente[1], 
            $datos_cliente[2], 
            $datos_cliente[3], 
            $datos_cliente[4], 
            $datos_cliente[5]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_CLIENTE($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_CLIENTE(?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("i", $id);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }
}
?>
