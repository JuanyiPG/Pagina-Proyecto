 DELIMITER //
 create trigger actualizar_empleado after update on empleado 
 for each row begin 
 
 if old.direccion_empleado <> new.direccion_empleado then 
insert into historial_empleados (id_empleado, campo_modificado, valor_anterior, valor_nuevo, fecha_modificacion )
values (old.id_empleado, 'direccion_empleado', old.direccion_empleado, new.direccion_empleado, now());
end if; 

if old.telefono_empleado <> new.telefono_empleado then 
insert into historial_empleado (id_empleado, campo_modificado, valor_anterior, valor_nuevo, fecha_modificacion)
values (old.id_empleado, 'telefono_empleado', old.telefono_empleado, new.telefono_empleado, now()); 
end if; 

if old.correo_empleado <> new.correo_empleado then 
insert into historial_empleado (id_empleado, campo_modificado, valor_anterior, valor_nuevo, fecha_modificaion)
values (old.id_empleado, 'correo_empleado', old.correo_empleado, new.correo_empleado, now());
end if;

if old.Fecha_ing_empleado <> new.Fecha_ing_empleado then 
insert into historial_empleado (id_empleado, campo_modificado, valor_anterior, valor_nuevo, fecha_modificaion)
values (old.id_empleado, 'Fecha_ing_empleado', old.Fecha_ing_empleado, new.Fecha_ing_empleado, now());
end if;

if old.salario_empleado <> new.salario_empleado then 
insert into historial_empleado (id_empleado, campo_modificado, valor_anterior, valor_nuevo, fecha_modificaion)
values (old.id_empleado, 'salario_empleado', old.salario_empleado, new.salario_empleado, now());
end if;
end; 
 