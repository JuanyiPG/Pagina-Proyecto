<?php

class MATERIA_P
{
    public function INSERT_MATERIA_P($datos_materia_p)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Materia_prima(?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("issssiiss", 
            $datos_materia_p[0], 
            $datos_materia_p[1], 
            $datos_materia_p[2], 
            $datos_materia_p[3], 
            $datos_materia_p[4], 
            $datos_materia_p[5], 
            $datos_materia_p[6],
            $datos_materia_p[7],
            $datos_materia_p[8]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_MATERIA_P()
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Materia_prima()";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $materia_p = [];
        while ($row = $resultado->fetch_assoc()) {
            $materia_p[] = $row;
        }

        $resultado->free();
        return $materia_p; 
    }

    public function ACTUALIZAR_MATERIA_P($datos_materia_p)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Materia_prima(?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("issssiiss",
            $datos_materia_p[0], 
            $datos_materia_p[1], 
            $datos_materia_p[2], 
            $datos_materia_p[3], 
            $datos_materia_p[4], 
            $datos_materia_p[5], 
            $datos_materia_p[6],
            $datos_materia_p[7],
            $datos_materia_p[8]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_MATERIA_PRIMA($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_MATERIA_PRIMA(?)";
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
