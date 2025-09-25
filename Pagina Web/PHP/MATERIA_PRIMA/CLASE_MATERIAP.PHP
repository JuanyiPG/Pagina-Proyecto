<?php

class MATERIA_P
{
        private $conexion;

    public function __construct() {
        $this->conexion = new mysqli("localhost", "root", "basededatos", "luxi_fashon");

        if ($this->conexion->connect_error) {
            die("Error de conexión: " . $this->conexion->connect_error);
        }
    }

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

    public function CONSULTAR_MATERIA_P($search = "")
    {
        $con = new CONECTAR();
        $conexion = $con->conexion();

    $stmt = $conexion->prepare("CALL consultar_Materia_prima(?)");
    $stmt->bind_param("s", $search);
    $stmt->execute();

    $resultado = $stmt->get_result();
    $roles = $resultado->fetch_all(MYSQLI_ASSOC);

    $stmt->close();
    return $roles;
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
