 DELIMITER //
 create trigger act_empleado 
 after update on empleado 
 for each row 
 begin 
 if old.direccion_empleado <> new.direccion_empleado or  
    old.telefono_empleado <> new.telefono_empleado or  
    old.correo_empleado <> new.correo_empleado or   
    old.salario_empleado <> new.salario_empleado  or 
    old.Estado_empleado <> new.Estado_empleado then 
 insert into  historial_empleado (id_empleado, direccion_empl, telefono_emple, correo_emple, salario_emple, estado_emple)
 values (old.id_empleado, new.direccion_empleado, new.telefonoa_empleado, new.correo_empleado, new.salario_empleado, new.Estado_empleado);
end if ;
end;    
 DELIMITER; 

 DELIMITER //
create trigger act_cliente
after update on cliente
for each row 
begin 
if old.direccion_cliente <> new.direccion_cliente or 
   old.telefono_cliente <> new.telefono_cliente or 
   old.correo_cliente <> new.telefono_cliente then
insert into historial_cliente(id_cliente, direccion_cli, telefono_cli, correo_cli)
values (old.id_cliente, new.direccion_cliente, new.telefono_cliente, new.correo_cliente);
end if;
end; 
 DELIMITER; 
 
  DELIMITER //
create trigger act_materia_prima
after update on materia_prima
for each row 
begin 
if old.stock_actual_materia_p <> new.stock_actual_materia_p or 
old.stock_minimo_materia_p <> new.stock_minimo_materia_p or 
old.estado_materia_p <> new.estado_materia_p then
insert into historial_matpri(id_matpri, stock_actual_matpri, stock_min_matpri, estado_matpri )
values (old.materia_p, new.stock_actual_materia_p, new.stock_minimo_materia_p, new.estado_materia_p);
end if;
end; 
 DELIMITER;  

 DELIMITER //
create trigger act_pedido
after update on pedido 
for each row 
begin 
if old.color_p_pedido <> new.color_p_pedido or 
old.cant_producto <> new.cant_producto or 
old.estado_pedido <> new.estado_pedido then
insert into historial_pedido(id_pedido, color_p, cant_p, estado_p)
values (old.id_pedido, new.color_p_pedido, new.cant_producto, new.estado_pedido);
end if;
end; 
 DELIMITER;  

create triggers act_produccion
after update on produccion 
for each row 
begin 
if old.costo_mano_obra <> new.costo_mano_obra or 
old.valor_iva <> new.valor_iva then
insert into hostorial_produccion(id_produccion, costo_manobra, valor_iva)
values (old.id_produccion, new.costo_mano_obra, new.valor_iva); 
end if; 
end; 
 DELIMITER; 

 