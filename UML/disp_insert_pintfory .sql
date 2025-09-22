use PINTFORY

create table DISP_INSERT_CARGO
(id_disp_insert_cargo int primary key auto_increment not null, 
descrip_disp_insert_cargo varchar(100) not null,
fecha_disp_insert_cargo datetime not null
)

create table DISP_INSERT_EMPLE
(id_disp_insert_emple int primary key auto_increment not null,
descrip_disp_insert_emple varchar(100) not null,
fecha_disp_insert_emple datetime not null
)

create table DISP_INSERT_TELE_EMPLE
(id_disp_insert_tele_emple int primary key auto_increment not null,
descrip_disp_insert_tele_emple varchar(100) not null,
fecha_disp_insert_tele_emple datetime not null
)

create table DISP_INSERT_EMAIL_EMPLE
(id_disp_insert_email_emple int primary key auto_increment not null,
descrip_disp_insert_email_emple varchar(100) not null,
fecha_disp_insert_email_emple datetime not null
)

create table DISP_INSERT_LOGIN_EMPLE
(id_disp_insert_login_emple int primary key auto_increment not null,
descrip_disp_insert_login_emple varchar(100) not null,
fecha_disp_insert_login_emple datetime not null
)

create table DISP_INSERT_CLIEN
(id_disp_insert_clien int primary key auto_increment not null,
descrip_disp_insert_clien varchar(100) not null,
fecha_disp_insert_clien datetime not null
)

create table DISP_INSERT_TELE_CLIEN
(id_disp_insert_tele_clien int primary key auto_increment not null,
descrip_disp_insert_tele_clien varchar(100) not null,
fecha_disp_insert_tele_clien datetime not null
)

create table DISP_INSERT_EMAIL_CLIEN
(id_disp_insert_email_clien int primary key auto_increment not null,
descrip_disp_insert_email_clien varchar(100) not null,
fecha_disp_insert_email_clien datetime not null
)

create table DISP_INSERT_LOGIN_CLIEN
(id_disp_insert_login_clien int primary key auto_increment not null,
descrip_disp_insert_login_clien varchar(100) not null,
fecha_disp_insert_login_clien datetime not null
)

create table DISP_INSERT_PROVEE
(id_disp_insert_provee int primary key auto_increment not null,
descrip_disp_insert_clien_provee varchar(100) not null,
fecha_disp_insert_clien datetime not null
)

create table DISP_INSERT_TELE_PROVEE
(id_disp_insert_tele_provee int primary key auto_increment not null,
descrip_disp_insert_tele_provee varchar(100) not null,
fecha_disp_insert_tele_provee datetime not null
)

create table DISP_INSERT_EMAIL_PROVEE
(id_disp_insert_email_provee int primary key auto_increment not null,
descrip_disp_insert_email_provee varchar(100) not null,
fecha_disp_insert_email_provee datetime not null
)

create table DISP_INSERT_FACTU
(id_disp_insert_factu int primary key auto_increment not null,
descrip_disp_insert_factu varchar(100) not null,
fecha_disp_insert_factu datetime not null
)

create table DISP_INSERT_COMP
(id_disp_insert_comp int primary key auto_increment not null,
descrip_disp_insert_comp varchar(100) not null,
fecha_disp_insert_comp datetime not null
)

create table DISP_INSERT_VENT
(id_disp_insert_vent int primary key auto_increment not null,
descrip_disp_insert_vent varchar(100) not null,
fecha_disp_insert_vent datetime not null
)

create table DISP_INSERT_METO_PAGO
(id_disp_insert_meto_pago int primary key auto_increment not null,
descrip_disp_insert_meto_pago varchar(100) not null,
fecha_disp_insert_meto_pago datetime not null
)

create table DISP_INSERT_MATE_PRIM
(id_disp_insert_mate_prim int primary key auto_increment not null,
descrip_disp_insert_mate_prim varchar(100) not null,
fecha_disp_insert_mate_prim datetime not null
)

create table DISP_INSERT_ENTRA_MATE_PRIM
(id_disp_insert_entra_mate_prim int primary key auto_increment not null,
descrip_disp_insert_entra_mate_prim varchar(100) not null,
fecha_disp_insert_entra_mate_prim datetime not null
)

create table DISP_INSERT_SALID_MATE_PRIM
(id_disp_insert_salid_mate_prim int primary key auto_increment not null,
descrip_disp_insert_salid_mate_prim varchar(100) not null,
fecha_disp_insert_salid_mate_prim datetime not null
)

create table DISP_INSERT_PRODUC
(id_disp_insert_produc int primary key auto_increment not null,
descrip_disp_insert_produc varchar(100) not null,
fecha_disp_insert_produc datetime not null
)

create table DISP_INSERT_ENTRAD_PRODUC
(id_disp_insert_entrad_produc int primary key auto_increment not null,
descrip_disp_insert_entrad_produc varchar(100) not null,
fecha_disp_insert_entrad_produc datetime not null
)

create table DISP_INSERT_SALID_PRODUC
(id_disp_insert_salid_produc int primary key auto_increment not null,
descrip_disp_insert_salid_produc varchar(100) not null,
fecha_disp_insert_salid_produc datetime not null
)


DELIMITER //
Create trigger D_insert_cargo
after insert on CARGO
for each row
begin
insert into DISP_INSERT_CARGO (descrip_disp_insert_cargo, fecha_disp_insert_cargo)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;



DELIMITER //
Create trigger D_insert_emple
after insert on EMPLEADO
for each row
begin
insert into DISP_INSERT_EMPLE (descrip_disp_insert_emple, fecha_disp_insert_emple)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_tele_emple
after insert on TELE_EMPLE
for each row
begin
insert into DISP_INSERT_TELE_EMPLE (descrip_disp_insert_tele_emple, fecha_disp_insert_tele_emple)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_email_emple
after insert on EMAIL_EMPLE
for each row
begin
insert into DISP_INSERT_EMAIL_EMPLE (descrip_disp_insert_email_emple, fecha_disp_insert_email_emple)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_login_emple
after insert on LOGIN_EMPLE
for each row
begin
insert into DISP_INSERT_LOGIN_EMPLE (descrip_disp_insert_login_emple, fecha_disp_insert_login_emple)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_clien
after insert on CLIENTE
for each row
begin
insert into DISP_INSERT_CLIENTE (descrip_disp_insert_clien, fecha_disp_insert_clien)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_tele_clien
after insert on TELE_CLIEN
for each row
begin
insert into DISP_INSERT_TELE_CLIEN (descrip_disp_insert_tele_clien, fecha_disp_insert_tele_clien)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_email_clien
after insert on EMAIL_CLIEN
for each row
begin
insert into DISP_INSERT_EMAIL_CLIEN (descrip_disp_insert_email_clien, fecha_disp_insert_email_clien)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_login_clien
after insert on LOGIN_CLIEN
for each row
begin
insert into DISP_INSERT_LOGIN_CLIEN (descrip_disp_insert_login_clien, fecha_disp_insert_login_clien)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_provee
after insert on PROVEEDOR
for each row
begin
insert into DISP_INSERT_PROVEE (descrip_disp_insert_provee, fecha_disp_insert_provee)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_tele_provee
after insert on TELE_PROVEE
for each row
begin
insert into DISP_INSERT_TELE_PROVEE (descrip_disp_insert_tele_provee, fecha_disp_insert_tele_provee)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_email_provee
after insert on EMAIL_PROVEE
for each row
begin
insert into DISP_INSERT_EMAIL_PROVEE (descrip_disp_insert_email_provee, fecha_disp_insert_email_provee)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_factu
after insert on FACTURA
for each row
begin
insert into DISP_INSERT_factu (descrip_disp_insert_factu, fecha_disp_insert_factu)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_comp
after insert on COMPRA
for each row
begin
insert into DISP_INSERT_COMP (descrip_disp_insert_comp, fecha_disp_insert_comp)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_vent
after insert on VENTA
for each row
begin
insert into DISP_INSERT_VENT (descrip_disp_insert_vent, fecha_disp_insert_vent)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_meto_pago
after insert on METODO_PAGO
for each row
begin
insert into DISP_INSERT_METO_PAGO (descrip_disp_insert_meto_pago, fecha_disp_insert_meto_pago)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_mate_prim
after insert on MATERIA_PRIMA
for each row
begin
insert into DISP_INSERT_MATE_PRIM (descrip_disp_insert_mate_prim, fecha_disp_insert_mate_prim)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_entra_mate_prim
after insert on ENTRADA_MATE_PRIM
for each row
begin
insert into DISP_INSERT_ENTRA_MATE_PRIM (descrip_disp_insert_entra_mate_prim, fecha_disp_insert_entra_mate_prim)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_salid_mate_prim
after insert on SALIDA_MATE_PRIM
for each row
begin
insert into DISP_INSERT_SALID_MATE_PRIM (descrip_disp_insert_salid_mate_prim, fecha_disp_insert_salid_mate_prim)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_produc
after insert on PRODUCTO
for each row
begin
insert into DISP_INSERT_PRODUC (descrip_disp_insert_produc, fecha_disp_insert_produc)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_entra_produc
after insert on ENTRADA_PRODUCTO
for each row
begin
insert into DISP_INSERT_ENTRA_PRODUC (descrip_disp_insert_entra_produc, fecha_disp_insert_entra_produc)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;


DELIMITER //
Create trigger D_insert_salid_produc
after insert on SALIDA_PRODUCTO
for each row
begin
insert into DISP_INSERT_SALID_PRODUC (descrip_disp_insert_salid_produc, fecha_disp_insert_salid_produc)
values ("se ha insertado correctamente", now());
end //
DELIMITER ;

insert into CARGO
values('1C', 'Mesero');

SELECT * FROM DISP_INSERT_CARGO