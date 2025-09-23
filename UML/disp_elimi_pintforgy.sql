use pintforgy;

create table DISP_ELIMI_CARGO
(id_disp_elimi_cargo int primary key auto_increment not null,
id_carg varchar(10) not null,
fecha_carg datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_cargo
BEFORE DELETE ON CARGO
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_CARGO(id_carg, fecha_cargo)
    VALUES (OLD.id_cargo, NOW());
END ;
DELIMITER ;


create table DISP_ELIMI_EMPLEADO
(id_disp_elimi_emple int primary key auto_increment not null,
id_emplea int not null,
fecha_emplea datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_emple
BEFORE DELETE ON EMPLEADO
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_EMPLEADO(id_emplea, fecha_emplea)
    VALUES (OLD.id_emple, NOW());
END ;
DELIMITER ;



create table DISP_ELIMI_LOGIN_EMPLE
(id_disp_elimi_login_emple int primary key auto_increment not null,
id_login_emplea varchar(30) not null,
fecha_login_emplea datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_login_emple
BEFORE DELETE ON LOGIN_EMPLE
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_LOGIN_EMPLE (id_login_emplea, fecha_login_emplea)
    VALUES (OLD.id_login_emple, NOW());
END ;
DELIMITER ;


create table DISP_ELIMI_CLIENTE
(id_disp_elimi_cliente int primary key auto_increment not null,
id_client int not null,
fecha_client datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_cliente
BEFORE DELETE ON CLIENTE
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_CLIENTE(id_client, fecha_client)
    VALUES (OLD.id_clien, NOW());
END ;
DELIMITER ;


create table DISP_ELIMI_PROVEE
(id_disp_elimi_provee int primary key auto_increment not null,
id_proveed int not null,
fecha_proveed datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_provee
BEFORE DELETE ON PROVEEDOR
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_PROVEE (id_proveed, fecha_proveed)
    VALUES (OLD.id_provee, NOW());
END ;
DELIMITER ;


create table DISP_ELIMI_METODO_PAGO
(id_disp_elimi_meto_pago int primary key auto_increment not null,
id_metod_pago int not null,
fecha_metod_pago datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_metodo_pago
BEFORE DELETE ON METODO_PAGO
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_METODO_PAGO(id_metod_pago, fecha_metod_pago)
    VALUES (OLD.id_meto_pago, NOW());
END ;
DELIMITER ;


create table DISP_ELIMI_PRODUCTO
(id_disp_elimi_prod int primary key auto_increment not null,
cod_produc int not null,
fecha_produc datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_producto
BEFORE DELETE ON PRODUCTO
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_PRODUCTO(cod_produc, fecha_produc)
    VALUES (OLD.id_prod, NOW());
END ;
DELIMITER ;


create table DISP_ELIMI_ENTRADA_PRODUCTO
(id_disp_elimi_entra_prod int primary key auto_increment not null,
id_entra_produc int not null,
fecha_entra_produc datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_entrada_producto
BEFORE DELETE ON ENTRADA_PRODUCTO
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_ENTRADA_PRODUCTO (id_entra_produc,fecha_entra_produc)
    VALUES (OLD.id_entra_prod, NOW());
END ;
DELIMITER ;

create table DISP_ELIMI_DETALLE_fACTU
(id_disp_elimi_detalle_factu int primary key auto_increment not null,
id_detalle_factur int not null,
fecha_detalle_Factur datetime not null);

DELIMITER //
CREATE TRIGGER D_elimi_detalle_factu
BEFORE DELETE ON DETALLE_FACTURA
FOR EACH ROW
BEGIN
    INSERT INTO DISP_ELIMI_DETALLE_FACTURA (id_entra_detalle_factur,fecha_detalle_factur)
    VALUES (OLD.id_detalle_factu, NOW());
END ;
DELIMITER ;
