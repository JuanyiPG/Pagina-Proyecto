<?php

class PRODUCTO_T
{
        private $conexion;

    public function __construct() {
        $this->conexion = new mysqli("localhost", "root", "basededatos", "luxi_fashon");

        if ($this->conexion->connect_error) {
            die("Error de conexión: " . $this->conexion->connect_error);
        }
    }

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

    public function CONSULTAR_PRODUCTO_T($search = "")
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

    $stmt = $conexion->prepare("CALL consultar_Producto_terminado(?)");
    
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
