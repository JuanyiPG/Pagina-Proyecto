<?php

class FACTURA_C
{
    public function INSERT_FACTURA_C($datos_factura_c)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        
        $sql = "CALL insrt_Factura_compra(?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isissi", 
            $datos_factura_c[0], 
            $datos_factura_c[1], 
            $datos_factura_c[2], 
            $datos_factura_c[3], 
            $datos_factura_c[4], 
            $datos_factura_c[5]
        );

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function CONSULTAR_FACTURA_C()
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Factura_compra()";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $factura_c = [];
        while ($row = $resultado->fetch_assoc()) {
            $factura_c[] = $row;
        }

        $resultado->free();
        return $factura_c; 
    }

    public function ACTUALIZAR_FACTURA_C($datos_factura_c)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL actualizar_Factura_compra(?,?,?,?,?,?)";
        $stmt = $conexion->prepare($sql);

        if ($stmt === false) {
            die("Error en la preparación: " . $conexion->error);
        }

        $stmt->bind_param("isissi",
            $datos_factura_c[0], 
            $datos_factura_c[1], 
            $datos_factura_c[2], 
            $datos_factura_c[3], 
            $datos_factura_c[4], 
            $datos_factura_c[5]);

        $resultado = $stmt->execute();

        if (!$resultado) {
            die("Error al ejecutar: " . $stmt->error);
        }

        $stmt->close();
        return $resultado;
    }

    public function ELIMINAR_FACTURA_C($id)
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL ELIMINAR_FACTURA_COMPRA(?)";
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
