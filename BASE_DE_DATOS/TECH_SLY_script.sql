create database TECH_SLY;
use TECH_SLY;


 Create Table Empleado 
 ( Id_emple BIGINT PRIMARY KEY NOT NULL,
   Nom_emple VARCHAR (30) NOT NULL,
   fech_ingre_emple DATE NOT NULL,
   RH_emple VARCHAR (5) NOT NULL,
   salario_emple NUMERIC NOT NULL,
   fech_naci_emple DATE NOT NULL,
   direc_emple VARCHAR (30) NOT NULL,
   estado_emple BOOLEAN NOT NULL
 );

 create table Telef_empleado
 ( Id_telef_emple INT PRIMARY KEY NOT NULL,
   telef_emple_1 NUMERIC UNIQUE NOT NULL,
   Id_emple_fk_telef_emple BIGINT NOT NULL,
   CONSTRAINT Id_emple_fk_telef_emple FOREIGN KEY (Id_emple_fk_telef_emple) REFERENCES Empleado (Id_emple),
  estado_tele_emple BOOLEAN NOT NULL
 );

 create table Correo_emple
 ( Id_correo_emple INT PRIMARY KEY NOT NULL,
   correo_emple_1 VARCHAR (40) UNIQUE NOT NULL,
   Id_emple_fk_correo_emple BIGINT NOT NULL,
   CONSTRAINT Id_emple_fk_correo_emple FOREIGN KEY (Id_emple_fk_correo_emple) REFERENCES Empleado(Id_emple),
   estado_correo_emple BOOLEAN NOT NULL
 );

 create table Cliente(
  Id_cliente BIGINT PRIMARY KEY NOT NULL,
  Nom_cliente VARCHAR (30) NOT NULL,
  fecha_naci_clien DATE NOT NULL,
  ciudad_cliente VARCHAR (30) NOT NULL,
  estado_cliente  BOOLEAN NOT NULL
 );

 create table Telef_clien
 ( Id_telef_cliente INT PRIMARY KEY NOT NULL,
   telf_cliente_1 NUMERIC UNIQUE NOT NULL,
   Id_cliente_fk_telef_cliente BIGINT NOT NULL,
   CONSTRAINT Id_cliente_fk_telef_cliente FOREIGN KEY (Id_cliente_fk_telef_cliente) REFERENCES Cliente(Id_cliente),
   estado_telef_cliente BOOLEAN NOT NULL
 );

 create table correo_client
 (Id_correo_client INT PRIMARY KEY NOT NULL,
  correo_client_1  VARCHAR(40) UNIQUE NOT NULL,
  Id_cliente_fk_correo_client BIGINT NOT NULL,
  CONSTRAINT Id_cliente_fk_correo_client FOREIGN KEY (Id_cliente_fk_correo_client) REFERENCES Cliente(Id_cliente),
  Estado_correo_client BOOLEAN NOT NULL
 );
 
 create table Usuarios 
 (Id_usuario INT PRIMARY KEY NOT NULL,
 Nom_usuario VARCHAR(30)  NOT NULL,
  Contraseña VARCHAR(40) NOT NULL,
  estado_usuario BOOLEAN NOT NULL
 );
 
 Create table Usuari_emple
 ( Id_usu_emple INT PRIMARY KEY NOT NULL,
  Id_emple_fk_usuari_emple BIGINT NOT NULL,
  CONSTRAINT Id_emple_fk_usuari_emple FOREIGN KEY(Id_emple_fk_usuari_emple) REFERENCES Empleado (Id_emple)
  );
  
  create table usuari_cliente
  (Id_usu_clen INT PRIMARY KEY NOT NULL,
  Id_clien_fk_usuari_cliente BIGINT NOT NULL,
  CONSTRAINT Id_clien_fk_usuari_cliente FOREIGN KEY(Id_clien_fk_usuari_cliente) REFERENCES Cliente (Id_cliente)
  );
 
 create table Facturacion
 ( Cod_factu INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   fecha_factu DATE NOT NULL,
   IVA_factu BIGINT NOT NULL,
   subtotal_factu BIGINT,
   Total_factu BIGINT NOT NULL,
   Id_emple_fk_facturacion BIGINT NOT NULL,
   CONSTRAINT Id_emple_fk_facturacion FOREIGN KEY (Id_emple_fk_facturacion) REFERENCES Empleado(Id_emple),
   estado_facturacion BOOLEAN NOT NULL
 );
 
	 create  table Producto
	 ( Cod_produc INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	  Nom_produc VARCHAR (30) NOT NULL,
	   talla_producto VARCHAR (15) NOT NULL,
	   color_producto VARCHAR(10) NOT NULL,
	   Categoria_producto VARCHAR (30) NOT NULL,
	   Materi_produc VARCHAR (30) NOT NULL,
	   Medida_produc NUMERIC NOT NULL,
	   Cant_produc NUMERIC NOT NULL,
	   Cant_minima BIGINT NOT NULL,
	   valor_produc BIGINT NOT NULL,
	   estilo_producto VARCHAR  (30) NOT NULL,
	   descripcion_producto VARCHAR (50) NOT NULL,
	   estado_produ BOOLEAN NOT NULL
	 );
 
 create table Materia_prima
 (Id_materia INT PRIMARY KEY NOT NULL,
  Nom_materia_prima VARCHAR(40) NOT NULL,
  Tipo_material VARCHAR(30) NOT NULL,
  Color VARCHAR(30) NOT NULL,
  Stock_actual NUMERIC NOT NULL,
  Stock_minimo NUMERIC NOT NULL,
  Descripcion VARCHAR(50) NOT NULL,
  estado_materia BOOLEAN NOT NULL,
  Id_producto_fk_materia_prima INT NOT NULL,
  CONSTRAINT Id_producto_fk_materia_prima FOREIGN KEY (Id_producto_fk_materia_prima) REFERENCES Producto(Cod_produc)
 );
 
 create table Producto_MateriaPrima 
 (id_prod_materia INT PRIMARY KEY AUTO_INCREMENT,
  id_producto_fk_prod_materi INT NOT NULL,
  CONSTRAINT id_producto_fk_prod_materi FOREIGN KEY (id_producto_fk_prod_materi) REFERENCES Producto(Cod_produc),
  id_materia_fk_prod_materi INT NOT NULL,
  CONSTRAINT id_materia_fk_prod_materi FOREIGN KEY (id_materia_fk_prod_materi) REFERENCES Materia_prima(Id_materia),
  cantidad_utilizada NUMERIC NOT NULL,
  unidad VARCHAR(10) NOT NULL
 );

 
  create table Compra_materia_prima
 ( Id_compra_m INT PRIMARY KEY NOT NULL,
   cantidad_compra BIGINT NOT NULL,
   valor_compra BIGINT NOT NULL,
   descrip_compra VARCHAR(50) NOT NULL,
   fecha_compra DATE NOT NULL,
   Id_Materiaprima_fk_materia_c INT NOT NULL,
   CONSTRAINT Id_Materiaprima_fk_materia_c FOREIGN KEY(Id_Materiaprima_fk_materia_c) REFERENCES Materia_prima(Id_materia),
   Estado_compra_m BOOLEAN NOT NULL
 );

 create table Pedido
 ( Id_pedido INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   valor_pedido BIGINT NOT NULL,
   direccion_pedido VARCHAR (40) NOT NULL,
   fecha_soli_pedido DATE NOT NULL,
   Estado_pedido VARCHAR(30) NOT NULL,
   Id_cliente_fk_pedido BIGINT NOT NULL,
   CONSTRAINT Id_cliente_fk_pedido FOREIGN KEY (Id_cliente_fk_pedido) REFERENCES Cliente(Id_cliente)
 );
 
 create table Produccion
 (Id_produccion INT PRIMARY KEY NOT NULL,
 Fecha_ini_producc DATE NOT NULL,
 Fecha_fin_producc DATE NOT NULL,
 cantidad_producida INT NOT NULL,
 Estado_produccion VARCHAR(30) NOT NULL,
 Costo_total BIGINT NOT NULL,
 Id_producto_fk_produccion INT NOT NULL,
 CONSTRAINT Id_producto_fk_produccion FOREIGN KEY (Id_producto_fk_produccion) REFERENCES Producto(Cod_produc)
 );
 
 create table Metododepago
 (cod_metododepago INT PRIMARY KEY NOT NULL,
  medio_metododepago VARCHAR (20) NOT NULL,
  id_cliente_fk_metododepago BIGINT NOT NULL,
  CONSTRAINT id_cliente_fk_metododepago FOREIGN KEY (id_cliente_fk_metododepago) REFERENCES Cliente(Id_cliente),
  estado_metodopago BOOLEAN NOT NULL
 );

create table descrip_detalle
(  id_descrip INT NOT NULL,
   Id_pedido_fk_descrip_detalle INT NOT NULL,
   CONSTRAINT Id_pedido_fk_descrip_detalle FOREIGN KEY (Id_pedido_fk_descrip_detalle) REFERENCES Pedido(Id_pedido),
   Cod_produc_fk_descrip_detalle INT NOT NULL,
   CONSTRAINT Cod_produc_fk_descrip_detalle FOREIGN KEY (Cod_produc_fk_descrip_detalle) REFERENCES Producto(Cod_produc),
   cantidad BIGINT NOT NULL,
   Precio_unitario INT NOT NULL,
   sub_total BIGINT NOT NULL
);






 
 