<?php

class ROL
{
        private $conexion;

    public function __construct() {
        $this->conexion = new mysqli("localhost", "root", "basededatos", "luxi_fashon");

        if ($this->conexion->connect_error) {
            die("Error de conexión: " . $this->conexion->connect_error);
        }
    }

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

    public function CONSULTAR_ROL($search = "")
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

    $stmt = $conexion->prepare("CALL consultar_Rol(?)");

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

    public function ELIMINAR_ROLi($id)
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
