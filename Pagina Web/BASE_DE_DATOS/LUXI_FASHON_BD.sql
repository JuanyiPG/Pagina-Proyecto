CREATE    DATABASE LUXI_FASHON;
USE LUXI_FASHON;

CREATE TABLE Rol (
  id_rol INT PRIMARY KEY NOT NULL,
  nombre_rol VARCHAR (50) NOT NULL UNIQUE,
  descripcion VARCHAR(200) NOT NULL,
  estado VARCHAR(50) NOT NULL
);

CREATE TABLE Empleado (
  id_empleado INT PRIMARY KEY NOT NULL,
  nom_empleado VARCHAR(50) NOT NULL,
  direccion_empleado VARCHAR(100) NOT NULL,
  tipo_sangre VARCHAR(20) NOT NULL,
  telefono_empleado INT NOT NULL,
  correo_empleado VARCHAR(100) NOT NULL,
  Fecha_ing_empleado DATE NOT NULL,
  salario_empleado FLOAT NOT NULL,
  Estado_empleado VARCHAR(50) NOT NULL,
  id_rol_fk_empleado INT NOT NULL,
  CONSTRAINT id_rol_fk_empleado FOREIGN KEY (id_rol_fk_empleado) REFERENCES Rol (id_rol)
);

CREATE TABLE Cliente (
  id_cliente INT PRIMARY KEY NOT NULL,
  nom_cliente VARCHAR(50) NOT NULL,
  direccion_cliente VARCHAR(100) NOT NULL,
  telefono_cliente INT NOT NULL,
  correo_cliente VARCHAR(100) NOT NULL,
  id_rol_fk_cliente INT NOT NULL,
  CONSTRAINT id_rol_fk_cliente FOREIGN KEY (id_rol_fk_cliente) REFERENCES Rol (id_rol)
);

CREATE TABLE Factura_Venta (
  cod_factura_v INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  fecha_factura_v DATE NOT NULL,
  sub_total_factura_v BIGINT NOT NULL,
  iva_factura_v BIGINT NOT NULL,
  total_factura_v BIGINT NOT NULL,
  metodo_pago VARCHAR(50) NOT NULL,
  descuento INT NOT NULL,
  estado_factura_venta VARCHAR(50) NOT NULL,
  id_empleado_fk_factura INT NOT NULL,
  CONSTRAINT id_empleado_fk_factura FOREIGN KEY (id_empleado_fk_factura) REFERENCES Empleado (id_empleado)
);

CREATE TABLE Produccion (
  id_produccion INT PRIMARY KEY NOT NULL,
  fecha_inicio_produccion DATE NOT NULL,
  cantidad_producida NUMERIC NOT NULL,
  costo_mano_obra BIGINT NOT NULL,
  costo_total_materia_prima BIGINT NOT NULL,
  costo_iva BIGINT NOT NULL,
  costo_total_produccion BIGINT NOT NULL,
  fecha_fin_produccion DATE NOT NULL,
  estado_produccion VARCHAR(50) NOT NULL,
  id_empleado_fk_produccion INT NOT NULL,
  CONSTRAINT id_empleado_fk_produccion FOREIGN KEY(id_empleado_fk_produccion) REFERENCES Empleado (id_empleado)
);

CREATE TABLE Pedido (
  id_pedido INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  nom_p_edido VARCHAR(100) NOT NULL,
  talla_p_pedido VARCHAR(50) NOT NULL,
  color_p_pedido VARCHAR(50) NOT NULL,
  categoria_p_pedido VARCHAR(50) NOT NULL,
  material_p_pedido VARCHAR(100) NOT NULL,
  cant_producto NUMERIC NOT NULL,
  descripcion_p_pedido VARCHAR(200) NOT NULL,
  fecha_pedido DATE NOT NULL,
  sub_total_pedido BIGINT NOT NULL,
  valor_pedido BIGINT NOT NULL,
  estado_pedido VARCHAR(50) NOT NULL,
  id_cliente_fk_pedido INT NOT NULL,
  CONSTRAINT id_cliente_fk_pedido FOREIGN KEY (id_cliente_fk_pedido) REFERENCES Cliente (id_cliente),
  id_produccion_fk_pedido INT NOT NULL,
  CONSTRAINT id_produccion_fk_pedido FOREIGN KEY (id_produccion_fk_pedido) REFERENCES Produccion (id_produccion)
);

CREATE TABLE Producto_terminado (
  id_producto_t INT PRIMARY KEY NOT NULL,
  nombre_producto_t VARCHAR(50),
  descripcion_producto_t VARCHAR(200) NOT NULL,
  categoria_produ_t VARCHAR(50) NOT NULL,
  unidad_medida VARCHAR(50) NOT NULL,
  estado_producto_t VARCHAR(50) NOT NULL,
  id_produccion_fk_producto_terminado INT NOT NULL,
  CONSTRAINT id_produccion_fk_producto_terminado FOREIGN KEY (id_produccion_fk_producto_terminado) REFERENCES Produccion (id_produccion)
);

CREATE TABLE detalle_facturav_produtot (
  id_dettallef_p INT PRIMARY KEY NOT NULL,
  cod_factura_v_fk_detalle INT NOT NULL,
  CONSTRAINT cod_factura_v_fk_detalle FOREIGN KEY (cod_factura_v_fk_detalle) REFERENCES Factura_Venta (cod_factura_v),
  id_producto_t_fk_detalle INT NOT NULL,
  CONSTRAINT id_producto_t_fk_detalle FOREIGN KEY (id_producto_t_fk_detalle) REFERENCES Producto_terminado (id_producto_t),
  descripcion VARCHAR(200) NOT NULL
);

CREATE TABLE Materia_prima (
  id_materia_p INT PRIMARY KEY NOT NULL,
  nom_materia_p VARCHAR (50) NOT NULL,
  color_materia_p VARCHAR (50) NOT NULL,
  categoria_mp VARCHAR (50) NOT NULL,
  tipo_material_materia_p VARCHAR(100),
  stock_actual_materia_p NUMERIC NOT NULL,
  stock_minimo_materia_p NUMERIC NOT NULL,
  descripcion_materia_p VARCHAR(200) NOT NULL,
  estado_materia_p VARCHAR(50) NOT NULL
);

CREATE TABLE Factura_compra (
  cod_factura_compra INT PRIMARY KEY NOT NULL,
  fecha_factura_compra DATE NOT NULL,
  total_faactura_compra BIGINT NOT NULL,
  metododepago_factura_compra VARCHAR(50) NOT NULL,
  estado_factura_compra VARCHAR(50) NOT NULL,
  id_empleado_fk_factura_compra INT NOT NULL,
  CONSTRAINT id_empleado_fk_factura_compra FOREIGN KEY (id_empleado_fk_factura_compra) REFERENCES Empleado(id_empleado)
);

CREATE TABLE Detalle_factuc_compra_m (
  id_detalle_fcm INT PRIMARY KEY NOT NULL,
  cod_factura_compra_fk_detalle_fcm INT NOT NULL,
  CONSTRAINT cod_factura_compra_fk_detalle_fcm FOREIGN KEY (cod_factura_compra_fk_detalle_fcm) REFERENCES Factura_compra(cod_factura_compra),
  id_materia_p_compra_fk_detalle_fcm INT NOT NULL,
  CONSTRAINT id_materia_p_compra_fk_detalle_fcm FOREIGN KEY (id_materia_p_compra_fk_detalle_fcm) REFERENCES Materia_prima (id_materia_p),
  cantidad_detalle_factu_fcm NUMERIC NOT NULL,
  descrion_factu_fcm VARCHAR(200) NOT NULL
);

CREATE TABLE Detalle_produccion_materiap_ (
  id_dettalle_produccion_materiap INT PRIMARY KEY NOT NULL,
  id_materia_p_fk_detalle_p_m INT  NOT NULL,
  CONSTRAINT id_materia_p_fk_detalle_p_m FOREIGN KEY (id_materia_p_fk_detalle_p_m) REFERENCES Materia_prima (id_materia_p),
  id_produccion_fk_detalle_p_m INT NOT NULL,
  CONSTRAINT id_produccion_fk_detalle_p_m FOREIGN KEY (id_produccion_fk_detalle_p_m) REFERENCES Produccion (id_produccion),
  descripcion VARCHAR(200) NOT NULL
);
Select * from Rol

