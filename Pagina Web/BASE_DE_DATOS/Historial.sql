/*----------ACTUALIZAR---------------------------*/
CREATE TABLE historial_empleados (
id_historial_emple int primary key auto_increment,
id_empleado int not null,
direccion varchar(100),
telefono int,
correo varchar(100),
salario float, 
estado varchar(100),
fecha_modificacion datetime not null default current_timestamp on update current_timestamp
); 

CREATE TABLE historial_cliente (
id_historial_cli int primary key auto_increment,
id_cliente int not null, 
direccion_cli varchar(100),
telefono_cli int,
correo_cli varchar(100),
fecha_modificacion datetime not null default current_timestamp on update current_timestamp
);

CREATE TABLE historial_matpri (
id_historial_matpri int primary key auto_increment,
id_matpri int not null, 
stock_actual_matpri varchar(100),
stock_min_matpri decimal(10,0),
 estado_matpri decimal(10,0),
fecha_modificacion datetime not null default current_timestamp on update current_timestamp
);

CREATE TABLE historial_pedido (
id_historial_pedido int primary key auto_increment,
id_pedido int not null, 
color_p varchar(50),
cant_p decimal(10,0), 
estado_p varchar(50),
fecha_modificacion datetime not null default current_timestamp on update current_timestamp
);

CREATE TABLE historial_produccion (
id_historial_produccion int primary key auto_increment,
id_produccion int not null, 
costo_manobra bigint, 
valor_iva bigint,
fecha_modificacion datetime not null default current_timestamp on update current_timestamp
); 

/*----------INSERTAR---------------------------*/
CREATE TABLE historial_insert_empleado (
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);

CREATE TABLE historial_insert_factura_c (
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);

CREATE TABLE historial_insert_factura_v (
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);

CREATE TABLE historial_insert_matepri(
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);

CREATE TABLE historial_insert_pedido(
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);

/*----------ELIMINAR---------------------------*/

CREATE TABLE historial_delete_empleado(
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);

CREATE TABLE historial_delete_cliente(
id_historial_ins_emple int key auto_increment,
acccion varchar(100),
fecha_modificacion datetime not null
);



