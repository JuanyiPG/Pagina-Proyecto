<?php

class FACTURA_V
{
    public function INSERT_FACTURA_V($datos_factura_v)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Factura_Venta(?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isiiisisi", 
            $datos_factura_v[0], 
            $datos_factura_v[1], 
            $datos_factura_v[2], 
            $datos_factura_v[3], 
            $datos_factura_v[4], 
            $datos_factura_v[5],
            $datos_factura_v[6],
            $datos_factura_v[7],
            $datos_factura_v[8]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_FACTURA_V($filtro = '')
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $filtro = $conexion -> real_escape_string($filtro);

        $sql = "CALL consultar_Factura_Venta('$filtro')";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $factura_v = [];
        while ($row = $resultado->fetch_assoc()) {
            $factura_v[] = $row;
        }

        $resultado->free();
        $conexion->next_result();
        return $factura_v; 
    }

    public function ACTUALIZAR_FACTURA_V($datos_factura_v)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Factura_Venta(?,?,?,?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isiiisisi",
            $datos_factura_v[0], 
            $datos_factura_v[1], 
            $datos_factura_v[2], 
            $datos_factura_v[3], 
            $datos_factura_v[4], 
            $datos_factura_v[5],
            $datos_factura_v[6],
            $datos_factura_v[7],
            $datos_factura_v[8]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_FACTURA_V($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_FACTURA_VENTA(?)";
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
