CREATE DATABASE IF NOT EXISTS LUXY_FASHION;
USE LUXY_FASHION;

-- =========================
-- TABLA ROL
-- =========================
CREATE TABLE Rol (
  id_rol INT PRIMARY KEY AUTO_INCREMENT,
  nom_rol VARCHAR(200) NOT NULL
);

-- =========================
-- TABLA EMPLEADO
-- =========================
CREATE TABLE Empleado (
  id_emple INT PRIMARY KEY AUTO_INCREMENT,
  nom_emple VARCHAR(50) NOT NULL,
  tel_emple VARCHAR(20) NOT NULL,
  correo_emple VARCHAR(100) NOT NULL UNIQUE,
  dir_emple VARCHAR(100) NOT NULL,
  rh_emple VARCHAR(20) NOT NULL,
  fecha_naci_emple DATE NOT NULL,
  tipo_ident VARCHAR(100) NOT NULL,
  num_ident VARCHAR(30) NOT NULL,
  fecha_ing_emple DATE NOT NULL,
  salari_emple DECIMAL(10,2) NOT NULL,
  estado_emple VARCHAR(50) NOT NULL
);

-- =========================
-- TABLA CLIENTE
-- =========================
CREATE TABLE Cliente (
  id_clien INT PRIMARY KEY AUTO_INCREMENT,
  nom_clien VARCHAR(50) NOT NULL,
  dir_clien VARCHAR(100) NOT NULL,
  tel_clien VARCHAR(20) NOT NULL,
  correo_clien VARCHAR(100) NOT NULL UNIQUE,
);

-- =========================
-- TABLA USUARIOS
-- =========================
CREATE TABLE usuario (
  id_usuario INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(255) NOT NULL,
  id_emple_fk_usuario INT NULL,
  id_clien_fk_usuario INT NULL,
  id_rol_fk_usuario INT NOT NULL,
  CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol_fk_usuario) REFERENCES Rol(id_rol),
  CONSTRAINT fk_usuario_emple FOREIGN KEY (id_emple_fk_usuario) REFERENCES Empleado(id_emple) ON DELETE CASCADE,
  CONSTRAINT fk_usuario_clien FOREIGN KEY (id_clien_fk_usuario) REFERENCES Cliente(id_clien) ON DELETE CASCADE
);


--    TABLA PEDIDO, si solo noti a admin
DELIMITER //
CREATE TABLE Pedido (
  id_pedido INT PRIMARY KEY AUTO_INCREMENT,
  nom_ped VARCHAR(100) NOT NULL,
  talla_ped VARCHAR(50) NOT NULL,
  color_ped VARCHAR(50) NOT NULL,
  categoria_ped VARCHAR(50) NOT NULL,
  material_ped VARCHAR(100) NOT NULL,
  cant_ped NUMERIC NOT NULL,
  desc_ped VARCHAR(200) NOT NULL,
  fecha_ped DATE NOT NULL,
  subtotal_ped DECIMAL(12,2) NOT NULL,
  valor_ped DECIMAL(12,2) NOT NULL,
  estado_ped VARCHAR(50) NOT NULL,
  metodo_pago VARCHAR(50) NOT NULL,
  id_clien_fk_ped INT NOT NULL,
  CONSTRAINT fk_pedido_clien FOREIGN KEY (id_clien_fk_ped) REFERENCES Cliente(id_clien)
);
//

--    TABLA FACTURA VENTA, si
DELIMITER //
CREATE TABLE Factura_venta (
  id_factuv INT PRIMARY KEY AUTO_INCREMENT,
  fecha_factuv DATE NOT NULL,

  subtotal_factuv DECIMAL(12,2) NOT NULL,
  iva_factuv DECIMAL(12,2) NOT NULL,
  total_factuv DECIMAL(12,2) NOT NULL,

  metodo_pago_factuv VARCHAR(50) NOT NULL,
  descu_factuv DECIMAL(12,2) DEFAULT 0,
  estado_factuv VARCHAR(50) NOT NULL,

  id_emple_fk_factuv INT NOT NULL,
  CONSTRAINT fk_factuv_emple
    FOREIGN KEY (id_emple_fk_factuv) REFERENCES Empleado(id_emple),

  id_clien_fk_factuv INT NOT NULL,
  CONSTRAINT fk_factuv_clien
    FOREIGN KEY (id_clien_fk_factuv) REFERENCES Cliente(id_clien),

  id_pedido_fk_factuv INT NOT NULL,
  CONSTRAINT fk_factuv_pedido
    FOREIGN KEY (id_pedido_fk_factuv) REFERENCES Pedido(id_pedido)
);

//

--    TABLA ABONO (NUEVA), si 
DELIMITER //
CREATE TABLE Abono (
  id_abono INT PRIMARY KEY AUTO_INCREMENT,
  fecha_abono DATE NOT NULL,
  monto_abono BIGINT NOT NULL,
  metodo_pago VARCHAR(50) NOT NULL,
  descripcion VARCHAR(200) NOT NULL,

  id_pedido_fk_abono INT NOT NULL,
  CONSTRAINT fk_abono_pedido FOREIGN KEY (id_pedido_fk_abono) REFERENCES Pedido( id_pedido)
);
//

--    TABLA MATERIA PRIMA, si
DELIMITER //
CREATE TABLE Materia_prima (
  id_matp INT PRIMARY KEY AUTO_INCREMENT,
  nom_matp VARCHAR(50) NOT NULL,
  color_matp VARCHAR(50) NOT NULL,
  categoria_matp VARCHAR(50) NOT NULL,
  tipo_matp VARCHAR(100),
  stock_act_matp NUMERIC NOT NULL,
  stock_min_matp NUMERIC NOT NULL,
  desc_matp VARCHAR(200) NOT NULL,
  estado_matp VARCHAR(50) NOT NULL
);
//

--    TABLA PRODUCCION, si
DELIMITER //
CREATE TABLE Produccion (
  id_producc INT PRIMARY KEY AUTO_INCREMENT,
  fecha_ini_producc DATE NOT NULL,
  cant_producc NUMERIC NOT NULL,
  costo_mano_obra_producc BIGINT NOT NULL,
  costo_mat_producc BIGINT NOT NULL,
  costo_total_producc BIGINT NOT NULL,
  fecha_fin_producc DATE NOT NULL,
  estado_producc VARCHAR(50) NOT NULL,

  id_emple_fk_producc INT NOT NULL,
  CONSTRAINT fk_producc_emple FOREIGN KEY (id_emple_fk_producc) REFERENCES Empleado(id_emple),

  id_pedido_fk_producc INT NULL,
  CONSTRAINT fk_producc_pedido FOREIGN KEY (id_pedido_fk_producc) REFERENCES Pedido(id_pedido),

  id_matp_fk_producc INT NOT NULL,
  CONSTRAINT fk_producc_matp FOREIGN KEY (id_matp_fk_producc) REFERENCES Materia_prima(id_matp)
);
//

--    TABLA PRODUCTO
DELIMITER //
CREATE TABLE Producto (
  id_produc INT PRIMARY KEY AUTO_INCREMENT,
  link_produc VARCHAR(500) NOT NULL,
  nom_produc VARCHAR(50) NOT NULL,
  desc_produc VARCHAR(200) NOT NULL,
  categoria_produc VARCHAR(50) NOT NULL,
  unid_med_produc VARCHAR(50) NOT NULL,
  estado_produc VARCHAR(50) NOT NULL,

  id_producc_fk_produc INT NOT NULL,
  CONSTRAINT fk_produc_producc FOREIGN KEY (id_producc_fk_produc) REFERENCES Produccion(id_producc)
);
//

--    DETALLE FACTURA VENTA, no
DELIMITER //
CREATE TABLE Det_factv_produc (
  id_det INT PRIMARY KEY AUTO_INCREMENT,
  id_factuv_fk INT NOT NULL,
  CONSTRAINT fk_det_factuv FOREIGN KEY (id_factuv_fk) REFERENCES Factura_venta(id_factuv),

  id_produc_fk INT NOT NULL,
  CONSTRAINT fk_det_produc FOREIGN KEY (id_produc_fk) REFERENCES Producto(id_produc),

  desc_det VARCHAR(200) NOT NULL
);
//

--    FACTURA COMPRA, si
DELIMITER //
CREATE TABLE Factura_compra (
  id_factuc INT PRIMARY KEY AUTO_INCREMENT,
  fecha_factuc DATE NOT NULL,
  total BIGINT NOT NULL,
  metodo_pago VARCHAR(50) NOT NULL,
  estado VARCHAR(50) NOT NULL,

  id_emple_fk INT NOT NULL,
  CONSTRAINT fk_factuc_emple FOREIGN KEY (id_emple_fk) REFERENCES Empleado(id_emple)
);
//

--    DETALLE FACTURA COMPRA, si
DELIMITER //
CREATE TABLE Det_factuc_matp (
  id_det_fcm INT PRIMARY KEY AUTO_INCREMENT,
  id_factuc_fk INT NOT NULL,
  CONSTRAINT fk_det_factuc FOREIGN KEY (id_factuc_fk) REFERENCES Factura_compra(id_factuc),

  id_matp_fk INT NOT NULL,
  CONSTRAINT fk_det_matp FOREIGN KEY (id_matp_fk) REFERENCES Materia_prima(id_matp),

  cant NUMERIC NOT NULL,
  desc_det VARCHAR(200) NOT NULL
);
//

--     DETALLE MATERIA PRIMA EN PRODUCCION, no
DELIMITER //
CREATE TABLE Det_producc_matp (
  id_det_pm INT AUTO_INCREMENT PRIMARY KEY,
  id_matp_fk INT NOT NULL,
  id_producc_fk INT NOT NULL,
  desc_det VARCHAR(200) NOT NULL,
  CONSTRAINT fk_detpm_matp FOREIGN KEY (id_matp_fk) REFERENCES Materia_prima(id_matp),
  CONSTRAINT fk_detpm_producc FOREIGN KEY (id_producc_fk) REFERENCES Produccion(id_producc)
);
//
DELIMITER ;
