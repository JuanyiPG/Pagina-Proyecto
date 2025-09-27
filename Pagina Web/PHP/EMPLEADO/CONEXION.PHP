<?php
    class CONECTAR
        {
            private $servidor="localhost";
            private $usuario="root";
            private $password="Subdi02050.";
            private $basedatos="LUXI_FASHON";
          

            public function conexion()
            {
                $conexion=mysqli_connect($this->servidor,$this->usuario,$this->password,$this->basedatos);
                return $conexion;
            }
        }
?>