<?php

class ROL
{
    public function INSERT_ROL($datos_rol)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Rol(?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isss", 
            $datos_rol[0], 
            $datos_rol[1], 
            $datos_rol[2], 
            $datos_rol[3]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_ROL($filtro = '')
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $filtro = $conexion->real_escape_string($filtro);

        $sql = "CALL consultar_Rol('$filtro')";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $producto_t = [];
        while ($row = $resultado->fetch_assoc()) {
            $producto_t[] = $row;
        }

        $resultado->free();
        $conexion->next_result();
        return $producto_t; 
    }

    public function ACTUALIZAR_ROL($datos_rol)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Rol(?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isss",
            $datos_rol[0], 
            $datos_rol[1], 
            $datos_rol[2], 
            $datos_rol[3]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_ROL($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_ROLi(?)";
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
