<?php

class PRODUCCION
{
    public function INSERT_PRODUCCION($datos_produccion)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Produccion(?,?,?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isiiiiissii", 
            $datos_produccion[0], 
            $datos_produccion[1], 
            $datos_produccion[2], 
            $datos_produccion[3], 
            $datos_produccion[4], 
            $datos_produccion[5],
            $datos_produccion[6],
            $datos_produccion[7],
            $datos_produccion[8],
            $datos_produccion[9],
            $datos_produccion[10]

        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_PRODUCCION()
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Produccion()";
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

    public function ACTUALIZAR_PRODUCCION($datos_produccion)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Produccion(?,?,?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isiiiiissii",
            $datos_produccion[0], 
            $datos_produccion[1], 
            $datos_produccion[2], 
            $datos_produccion[3], 
            $datos_produccion[4], 
            $datos_produccion[5],
            $datos_produccion[6],
            $datos_produccion[7],
            $datos_produccion[8],
            $datos_produccion[9],
            $datos_produccion[10]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_PRODUCCION($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_PRODUCCION(?)";
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
