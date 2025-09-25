<?php

class PEDIDO
{
    public function INSERT_PEDIDO($datos_pedido)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Pedido(?,?,?,?,?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isssssissiisi", 
            $datos_pedido[0], 
            $datos_pedido[1], 
            $datos_pedido[2], 
            $datos_pedido[3], 
            $datos_pedido[4], 
            $datos_pedido[5],
            $datos_pedido[6],
            $datos_pedido[7],
            $datos_pedido[8],
            $datos_pedido[9],
            $datos_pedido[10],
            $datos_pedido[11],
            $datos_pedido[12]

        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_PEDIDO()
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Pedido()";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $produccion = [];
        while ($row = $resultado->fetch_assoc()) {
            $produccion[] = $row;
        }

        $resultado->free();
        return $produccion; 
    }

    public function ACTUALIZAR_PEDIDO($datos_pedido)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Pedido(?,?,?,?,?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isssssissiisi",
            $datos_pedido[0], 
            $datos_pedido[1], 
            $datos_pedido[2], 
            $datos_pedido[3], 
            $datos_pedido[4], 
            $datos_pedido[5],
            $datos_pedido[6],
            $datos_pedido[7],
            $datos_pedido[8],
            $datos_pedido[9],
            $datos_pedido[10],
            $datos_pedido[11],
            $datos_pedido[12]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_PEDIDO($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_PEDIDO(?)";
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
