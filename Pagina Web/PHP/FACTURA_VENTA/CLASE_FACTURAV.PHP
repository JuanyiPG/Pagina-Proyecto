<?php

class FACTURA_V
{
        private $conexion;

    public function __construct() {
        $this->conexion = new mysqli("localhost", "root", "basededatos", "luxi_fashon");

        if ($this->conexion->connect_error) {
            die("Error de conexión: " . $this->conexion->connect_error);
        }
    }
    
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

    public function CONSULTAR_FACTURA_V($search = "")
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

        $stmt = $conexion->prepare("CALL consultar_Factura_Venta(?)");

        if ($stmt === false ){
        die("Error en la preparacion:" . $this->conexion->error);
        }

    $stmt->bind_param("s", $search);
    $stmt->execute();

    $resultado = $stmt->get_result();
    $roles = $resultado->fetch_all(MYSQLI_ASSOC);

    $stmt->close();
    return $roles; 
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
