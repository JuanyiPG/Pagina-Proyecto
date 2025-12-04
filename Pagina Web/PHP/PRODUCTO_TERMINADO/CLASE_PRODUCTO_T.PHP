<?php

class PRODUCTO_T
{
    public function INSERT_PRODUCTO_T($datos_producto_t)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Producto_terminado(?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isssssi", 
            $datos_producto_t[0], 
            $datos_producto_t[1], 
            $datos_producto_t[2], 
            $datos_producto_t[3], 
            $datos_producto_t[4], 
            $datos_producto_t[5], 
            $datos_producto_t[6]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_PRODUCTO_T($filtro = '')
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $filtro = $conexion->real_escape_string($filtro);

        $sql = "CALL Consultar_producto_terminado('$filtro')";
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

    public function ACTUALIZAR($datos_producto_t)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Producto_terminado(?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isssssi",
            $datos_producto_t[0], 
            $datos_producto_t[1], 
            $datos_producto_t[2], 
            $datos_producto_t[3], 
            $datos_producto_t[4], 
            $datos_producto_t[5], 
            $datos_producto_t[6]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_PRODUCTO_T(?)";
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
