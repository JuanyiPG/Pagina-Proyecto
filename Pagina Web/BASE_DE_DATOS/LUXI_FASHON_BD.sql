CREATE DATABASE LUXI_FASHON;
USE LUXI_FASHON;

create table rol (
  id_rol int primary key not null,
  nom_rol varchar(50) not null,
  desc_rol varchar(200) not null,
  estado varchar(50) not null
);

create table emple (
  id_emple int primary key not null,
  nom_emple varchar(50) not null,
  dir_emple varchar(100) not null,
  tipo_sangre varchar(20) not null,
  tel_emple varchar(20) not null,
  correo_emple varchar(100) not null,
  fecha_ing date not null,
  salario float not null,
  estado_emple varchar(50) not null,
  usuario varchar(50) not null,
  contras varchar(100) not null,
  id_rol_fk int not null,
  constraint fk_emple_rol foreign key (id_rol_fk) references rol (id_rol)
);

create table clien (
  id_clien int primary key not null,
  nom_clien varchar(50) not null,
  dir_clien varchar(100) not null,
  tel_clien varchar(20) not null,
  correo_clien varchar(100) not null,
  usuario varchar(50) not null,
  contras varchar(100) not null,
  id_rol_fk int not null,
  constraint fk_clien_rol foreign key (id_rol_fk) references rol (id_rol)
);

create table fact_venta (
  id_factv int primary key auto_increment not null,
  fecha date not null,
  subtotal bigint not null,
  iva bigint not null,
  total bigint not null,
  metodo_pago varchar(50) not null,
  descu int not null,
  estado varchar(50) not null,
  id_emple_fk int not null,
  constraint fk_factv_emple foreign key (id_emple_fk) references emple (id_emple)
);

create table pedido (
  id_pedido int primary key not null,
  nom_ped varchar(100) not null,
  talla varchar(50) not null,
  color varchar(50) not null,
  categoria varchar(50) not null,
  material varchar(100) not null,
  cant numeric not null,
  desc_ped varchar(200) not null,
  fecha date not null,
  subtotal bigint not null,
  valor bigint not null,
  estado varchar(50) not null,
  id_clien_fk int not null,
  constraint fk_pedido_clien foreign key (id_clien_fk) references clien (id_clien)
);

create table producc (
  id_producc int primary key not null,
  fecha_ini date not null,
  cant_prod numeric not null,
  costo_mano_obra bigint not null,
  costo_mat bigint not null,
  costo_iva bigint not null,
  costo_total bigint not null,
  fecha_fin date not null,
  estado varchar(50) not null,
  id_emple_fk int not null,
  constraint fk_producc_emple foreign key (id_emple_fk) references emple (id_emple),
  id_pedido_fk int not null,
  constraint fk_producc_pedido foreign key (id_pedido_fk) references pedido (id_pedido)
);

create table produc_term (
  id_produc int primary key not null,
  nom_produc varchar(50) not null,
  desc_produc varchar(200) not null,
  categoria varchar(50) not null,
  unid_med varchar(50) not null,
  estado varchar(50) not null,
  id_producc_fk int not null,
  constraint fk_produc_producc foreign key (id_producc_fk) references producc (id_producc)
);

create table det_factv_produc (
  id_det int primary key not null,
  id_factv_fk int not null,
  constraint fk_det_factv foreign key (id_factv_fk) references fact_venta (id_factv),
  id_produc_fk int not null,
  constraint fk_det_produc foreign key (id_produc_fk) references produc_term (id_produc),
  desc_det varchar(200) not null
);

create table matp (
  id_matp int primary key not null,
  nom_matp varchar(50) not null,
  color varchar(50) not null,
  categoria varchar(50) not null,
  tipo varchar(100),
  stock_act numeric not null,
  stock_min numeric not_

Select * from Rol

