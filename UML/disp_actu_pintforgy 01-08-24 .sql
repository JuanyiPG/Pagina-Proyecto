use pintforgy;

create table DISP_ACTU_CARGO
(id_disp_actu_cargo int primary key auto_increment not null,
id_carg varchar (30) not null,
nom_carg varchar (30) not null);

DELIMITER //
create trigger D_ACTU_CARGO
after update on CARGO
for each row
begin
    insert into DISP_ACTU_CARGO (id_carg, nom_carg)
    values (new.id_cargo, new.nom_cargo);
end //
DELIMITER ;



create table DISP_ACTU_EMPLE
(id_disp_actu_emple int primary key auto_increment not null,
id_emplea int not null,
nom_emplea varchar (30) not null,
rh_emplea varchar(10) not null,
numb_tele_emplea float not null,
nom_email_emplea varchar(30) not null,
salario_emplea float not null,
fechanaci_emplea date not null, 
fechaentra_emplea date not null, 
dire_emplea varchar (30) not null,
id_cargo_fk_emplea varchar (30) not null,
constraint id_cargo_fk_emplea foreign key (id_cargo_fk_emplea) references CARGO (id_cargo));

DELIMITER //
create trigger D_ACTU_EMPLE
after update on EMPLEADO
for each row
begin
    insert into DISP_ACTU_EMPLE (id_emplea, nom_emplea, rh_emplea, numb_tele_emplea, nom_email_emplea, salario_emplea, fechanaci_emplea, fechaentra_emplea, dire_emplea, id_cargo_fk_emplea)
    values (new.id_emple, new.nom_emple, new.rh_emple, new.numb_tele_emple, new.nom_email_emple, new.salario_emple, new.fechanaci_emple, new.fechaentra_emple, new.dire_emple, new.id_cargo_fk_emple);
end //
DELIMITER ;


create table DISP_ACTU_LOGIN_EMPLE
(id_disp_actu_email_emple int primary key auto_increment not null,
nom_login_emplea int not null,
contra_login_emplea varchar (30) not null,
id_emple_fk_login_emplea int not null, 
constraint id_emple_fk_login_emplea foreign key (id_emple_fk_login_emplea) references EMPLEADO (id_emple));

DELIMITER //
create trigger D_ACTU_LOGIN_EMPLE
after update on LOGIN_EMPLE
for each row
begin
   insert into DISP_ACTU_LOGIN_EMPLE(nom_login_emplea,contra_login_emplea,id_emple_fk_login_emplea)
   values (new.nom_login_emple, new.contra_login_emple, new.id_emple_fk_login_emple);
end //
DELIMITER ;



create table DISP_ACTU_CLIEN
(id_disp_actu_clien int primary key auto_increment not null,
id_client int not null, 
nom_client varchar (30) not null,
dire_client varchar (30) not null,
numb_tele_client numeric not null,
nom_email_client varchar(30) not null,
id_emple_fk_client int not null,
constraint id_emple_fk_client foreign key (id_emple_fk_client) references EMPLEADO (id_emple));

DELIMITER //
create trigger D_ACTU_CLIEN
after update on CLIENTE
for each row
begin
   insert into DISP_ACTU_CLIEN (id_client,nom_client,dire_client, numb_tele_client, nom_email_client, id_emple_fk_client)
   values (new.id_clien ,new.nom_clien,new.dire_clien, new.numb_tele_clien, new.nom_email_clien, new.id_emple_fk_clien);
end //
DELIMITER ;



create table DISP_ACTU_PROVEE
(id_disp_actu_provee int primary key auto_increment not null,
id_proveed int not null, 
nom_proveed varchar (30) not null,
numb_tele_client numeric not null,
nom_email_client varchar(30) not null);

DELIMITER //
create trigger D_ACTU_PROVEE
after update on PROVEDOR
for each row
begin 
   insert into DISP_ACTU_PROVEE (id_proveed, nom_proveed, numb_tele_proveed, nom_email_proveed)
   values (new.id_provee, new.nom_provee, new.numb_tele_provee, new.nom_email_provee);
end //
DELIMITER ;

create table DISP_ACTU_FACTU_VENT
(id_disp_actu_factu_vent int primary key auto_increment not null,
id_factu_vent int not null,
nom_factu_vent varchar(30) not null,
fecha_factu_vent float not null,
id_emple_fk_factu_vent int not null, 
constraint id_emple_fk_factu_vent foreign key (id_emple_fk_factu_vent) references EMPLEADO (id_emple),
id_clien_fk_factu_vent int not null, 
constraint id_clien_fk_factu_vent foreign key (id_clien_fk_factu_vent) references CLIENTE (id_clien),
cod_prod_fk_factu_vent int not null, 
constraint cod_prod_fk_factu_vent foreign key (cod_prod_fk_factu_vent) references PRODUCTO (cod_prod));

DELIMITER //
create trigger D_ACTU_FACTU_VENT
after update on FACTURA_VENTA
for each row
begin
   insert into D_ACTU_FACTU_VENT (id_factu_vent, nom_factu_vent, fecha_factu_vent, id_emple_fk_factu_vent, id_clien_fk_factu_vent, cod_prod_fk_factu_vent)
   values (new.id_factu_vent, new.nom_factu_vent, new.fecha_factu_vent, new.id_emple_fk_factu_vent, new.id_clien_fk_factu_vent, new.cod_prod_fk_factu_vent);
end //
DELIMITER ;

create table DISP_ACTU_METO_PAGO
(id_disp_actu_meto_pago int primary key auto_increment not null,
id_metod_pago int not null,
nom_metod_pago varchar(30) not null,
valor_metod_pago float not null,
id_clien_fk_metod_pago int not null, 
constraint id_clien_fk_metod_pago foreign key (id_clien_fk_metod_pago) references CLIENTE (id_clien));

DELIMITER //
create trigger D_ACTU_METO_PAGO
after update on METODO_PAGO
for each row
begin
   insert into D_ACTU_METO_PAGO (id_metod_pago, nom_metod_pago, valor_metod_pago, id_clien_fk_metod_pago)
   values (new.id_meto_pago, new.nom_meto_pago, new.valor_meto_pago, new.id_clien_fk_meto_pago);
end //
DELIMITER ;

create table DISP_ACTU_PROD
(id_disp_actu_prod int primary key auto_increment not null,
id_produc int not null,
nom_produc varchar (20) not null,
can_min_produc numeric not null,
can_max_produc numeric not null,
val_produc numeric not null,
marc_produc varchar (20) not null,
id_provee_fk_produc int not null,
constraint id_provee_fk_produc foreign key (id_provee_fk_produc) references PROVEEDOR (id_provee),
id_emple_fk_produc int not null,
constraint id_emple_fk_produc foreign key (id_emple_fk_produc) references EMPLEADO (id_emple));

DELIMITER //
create trigger D_ACTU_PROD
after update on PRODUCTO
for each row
begin
   insert into D_ACTU_PROD (id_produc, nom_produc, can_min_produc, can_max_produc, val_produc, marc_produc, id_provee_fk_produc, id_emple_fk_produc)
   values (new.id_prod, new.nom_prod, new.can_min_prod, new.can_max_prod, new.val_produc, new.marc_prod, new.id_provee_fk_prod, new.id_emple_fk_prod);
end //
DELIMITER ;

create table DISP_ACTU_ENTRA_PROD 
(id_disp_actu_entra_prod int primary key auto_increment not null,
id_entra_produc int not null,
fecha_entra_produc date not null,
cant_entra_produc numeric not null,
valor_entra_produc float not null,
descrip_entra_produc varchar (20) not null,
id_prod_fk_entra_produc int not null,
constraint id_prod_fk_entra_produc foreign key (id_prod_fk_entra_produc) references PRODUCTO (id_prod));

DELIMITER //
create trigger D_ACTU_ENTRA_PROD
after update on ENTRADA_PRODUCTO
for each row
begin
	insert into D_ACTU_ENTRA_PROD (id_entra_produc, fecha_entra_produc, cant_entra_produc, valor_entra_produc, descrip_entra_produc, id_prod_fk_entra_produc)
	values (new.id_entra_prod, new.fecha_entra_prod, new.cant_entra_prod, new.valor_entra_prod, new.descrip_entra_prod, new.id_prod_fk_entra_prod);
end//
DELIMITER ;


create table DISP_ACTU_DETALLE_FACTU
(id_disp_actu_detalle_factu int primary key auto_increment not null,
id_detalle_factur int not null,
cant_detalle_factur varchar(30) not null,
estado_detalle_factur float not null,
subtotal_detalle_factur float not null,
id_clien_fk_detalle_factur int not null, 
constraint id_clien_fk_detalle_factur foreign key (id_clien_fk_detalle_factur) references CLIENTE (id_clien),
cod_prod_fk_detalle_factur int not null, 
constraint cod_prod_fk_detalle_factur foreign key (cod_prod_fk_detalle_factur) references PRODUCTO (cod_prod),
id_factu_vent_fk_detalle_factur int not null, 
constraint id_factu_vent_fk_detalle_factur foreign key (id_factu_vent_fk_detalle_factur) references FACTURA_VENTA (id_factu_vent));

DELIMITER //
create trigger D_ACTU_DETALLE_FACTU
after update on DETALLE_FACTURA
for each row
begin
   insert into D_ACTU_DETALLE_FACTU (id_detalle_factur, cant_detalle_factur, estado_detalle_factur, subtotal_detalle_factur, id_clien_fk_detalle_factur, cod_prod_fk_detalle_factur, id_factu_vent_fk_detalle_factur)
   values (new.id_detalle_factu, new.cant_detalle_factu, new.estado_detalle_factu, new.subtotal_detalle_factu, new.id_clien_fk_detalle_factu, new.cod_prod_fk_detalle_factu, new.id_factu_vent_detalle_factu);
end //
DELIMITER ;