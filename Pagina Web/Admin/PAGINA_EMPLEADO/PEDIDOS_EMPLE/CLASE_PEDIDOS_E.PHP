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

    public function CONSULTAR_FACTURA_V()
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $sql = "CALL consultar_Factura_Venta()";
        $resultado = $conexion->query($sql);

        if (!$resultado) {
            die("Error en la consulta: " . $conexion->error);
        }

        $factura_v = [];
        while ($row = $resultado->fetch_assoc()) {
            $factura_v[] = $row;
        }

        $resultado->free();
        return $factura_v; 
    }
}