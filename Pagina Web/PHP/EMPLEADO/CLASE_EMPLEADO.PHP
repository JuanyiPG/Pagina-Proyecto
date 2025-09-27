<?php

class EMPLEADO
{
    public function INSERT_EMPLEADO($datos_empleado)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Empleado(?,?,?,?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isssississsi", 
            $datos_empleado[0], 
            $datos_empleado[1], 
            $datos_empleado[2], 
            $datos_empleado[3], 
            $datos_empleado[4], 
            $datos_empleado[5], 
            $datos_empleado[6],
            $datos_empleado[7],
            $datos_empleado[8],
            $datos_empleado[9],
            $datos_empleado[10],
            $datos_empleado[11]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_EMPLEADO($filtro = '')
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Empleado('$filtro')";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $empleado = [];
        while ($row = $resultado->fetch_assoc()) {
            $empleado[] = $row;
        }

        $resultado->free();
        return $empleado; 
    }

    public function ACTUALIZAR_EMPLEADO($datos_empleado)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Empleado(?,?,?,?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isssississsi",
            $datos_empleado[0], 
            $datos_empleado[1], 
            $datos_empleado[2], 
            $datos_empleado[3], 
            $datos_empleado[4], 
            $datos_empleado[5], 
            $datos_empleado[6],
            $datos_empleado[7],
            $datos_empleado[8],
            $datos_empleado[9],
            $datos_empleado[10],
            $datos_empleado[11]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_EMPLEADO($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_EMPLEADO(?)";
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
