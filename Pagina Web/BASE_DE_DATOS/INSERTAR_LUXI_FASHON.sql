USE LUXI_FASHON;

DELIMITER $$


CREATE PROCEDURE insrt_Rol(
  IN insrt_id_rol INT,
  IN insrt_nombre_rol VARCHAR(50),
  IN insrt_descripcion VARCHAR(200),
  IN insrt_estado VARCHAR(50)
)
BEGIN
  INSERT INTO Rol (id_rol, nombre_rol, descripcion, estado)
  VALUES (insrt_id_rol, insrt_nombre_rol, insrt_descripcion, insrt_estado);
END$$

 INSERT INTO luxi_fashon.rol (id_rol, nombre_rol, descripcion, estado)
  VALUES (1, 'cliente', 'juan', 'activo');




CREATE PROCEDURE insrt_Empleado(
  IN insrt_id_empleado INT,
  IN insrt_nom_empleado VARCHAR(50),
  IN insrt_direccion_empleado VARCHAR(100),
  IN insrt_tipo_sangre VARCHAR(20),
  IN insrt_telefono_empleado INT,
  IN insrt_correo_empleado VARCHAR(100),
  IN insrt_Fecha_ing_empleado DATE,
  IN insrt_salario_empleado FLOAT,
  IN insrt_Estado_empleado VARCHAR(50),
  IN insrt_nom_usuario VARCHAR(50),
  IN insrt_contras VARCHAR (100),
  IN insrt_id_rol_fk_empleado INT
)
BEGIN
  INSERT INTO Empleado (id_empleado, nom_empleado, direccion_empleado, tipo_sangre,
    telefono_empleado, correo_empleado, Fecha_ing_empleado,
    salario_empleado, Estado_empleado,nom_usuario,contras, id_rol_fk_empleado)
  VALUES (insrt_id_empleado, insrt_nom_empleado, insrt_direccion_empleado, insrt_tipo_sangre,
    insrt_telefono_empleado, insrt_correo_empleado, insrt_Fecha_ing_empleado,
    insrt_salario_empleado, insrt_Estado_empleado,insrt_nom_usuario,insrt_contras, insrt_id_rol_fk_empleado);
END$$


CREATE PROCEDURE insrt_Cliente(
  IN insrt_id_cliente INT,
  IN insrt_nom_cliente VARCHAR(50),
  IN insrt_direccion_cliente VARCHAR(100),
  IN insrt_telefono_cliente INT,
  IN insrt_correo_cliente VARCHAR(100),
  IN insrt_nombre_usuari VARCHAR (50),
  IN insrt_contra VARCHAR(100),
  IN insrt_id_rol_fk_cliente INT
)
BEGIN
  INSERT INTO Cliente (id_cliente, nom_cliente, direccion_cliente,
    telefono_cliente, correo_cliente,nombre_usuari,contra, id_rol_fk_cliente)
  VALUES (insrt_id_cliente, insrt_nom_cliente, insrt_direccion_cliente,
    insrt_telefono_cliente, insrt_correo_cliente,insrt_nombre_usuari, insrt_contra,insrt_id_rol_fk_cliente);
END$$

INSERT INTO luxi_fashon.cliente (id_cliente, nom_cliente, direccion_cliente,
    telefono_cliente, correo_cliente,nombre_usuari,contra, id_rol_fk_cliente)
  VALUES (1, 'juan', 'calle 42 a bis sur',310254620, 'juan@gmail.com','Juani', 'juani321',1);


CREATE PROCEDURE insrt_Factura_Venta(
  IN insrt_cod_factura_v INT,
  IN insrt_fecha_factura_v DATE,
  IN insrt_sub_total_factura_v BIGINT,
  IN insrt_iva_factura_v BIGINT,
  IN insrt_total_factura_v BIGINT,
  IN insrt_metodo_pago VARCHAR(50),
  IN insrt_descuento INT,
  IN insrt_estado_factura_venta VARCHAR(50),
  IN insrt_id_empleado_fk_factura INT
)
BEGIN
  INSERT INTO Factura_Venta (cod_factura_v,fecha_factura_v, sub_total_factura_v, iva_factura_v,
    total_factura_v, metodo_pago, descuento, estado_factura_venta, id_empleado_fk_factura)
  VALUES (insrt_cod_factura_v,insrt_fecha_factura_v, insrt_sub_total_factura_v, insrt_iva_factura_v,
    insrt_total_factura_v, insrt_metodo_pago, insrt_descuento,
    insrt_estado_factura_venta, insrt_id_empleado_fk_factura);
END$$


CREATE  PROCEDURE insrt_Pedido(
  IN insrt_id_pedido INT,
  IN insrt_nom_p_edido VARCHAR(100),
  IN insrt_talla_p_pedido VARCHAR(50),
  IN insrt_color_p_pedido VARCHAR(50),
  IN insrt_categoria_p_pedido VARCHAR(50),
  IN insrt_material_p_pedido VARCHAR(100),
  IN insrt_cant_producto NUMERIC,
  IN insrt_descripcion_p_pedido VARCHAR(200),
  IN insrt_fecha_pedido DATE,
  IN insrt_sub_total_pedido BIGINT,
  IN insrt_valor_pedido BIGINT,
  IN insrt_estado_pedido VARCHAR(50),
  IN insrt_id_cliente_fk_pedido INT
  
)
BEGIN
  INSERT INTO Pedido (id_pedido,nom_p_edido, talla_p_pedido, color_p_pedido, categoria_p_pedido,
    material_p_pedido, cant_producto, descripcion_p_pedido, fecha_pedido,
    sub_total_pedido, valor_pedido, estado_pedido, id_cliente_fk_pedido)
  VALUES (insrt_id_pedido,nom_p_edido, insrt_talla_p_pedido, insrt_color_p_pedido, insrt_categoria_p_pedido,
    insrt_material_p_pedido, insrt_cant_producto, insrt_descripcion_p_pedido, insrt_fecha_pedido,
    insrt_sub_total_pedido, insrt_valor_pedido, insrt_estado_pedido,
    insrt_id_cliente_fk_pedido);
END$$


INSERT INTO luxi_fashon.pedido (id_pedido,nom_p_edido, talla_p_pedido, color_p_pedido, categoria_p_pedido,
    material_p_pedido, cant_producto, descripcion_p_pedido, fecha_pedido,
    sub_total_pedido, valor_pedido, estado_pedido, id_cliente_fk_pedido)
VALUES (5,'chaqueta','m','azul','chaquetas','algodon',5,'chaqueta con forro', '12-05-15', 50000, 50000, 'pendiente',1);


CREATE PROCEDURE insrt_Produccion(
  IN insrt_id_produccion INT,
  IN insrt_fecha_inicio_produccion DATE,
  IN insrt_cantidad_producida NUMERIC,
  IN insrt_costo_mano_obra BIGINT,
  IN insrt_costo_total_materia_prima BIGINT,
  IN insrt_costo_iva BIGINT,
  IN insrt_costo_total_produccion BIGINT,
  IN insrt_fecha_fin_produccion DATE,
  IN insrt_estado_produccion VARCHAR(50),
  IN insrt_id_empleado_fk_produccion INT,
  IN insrt_id_pedido_fk_produccion INT
)

BEGIN
  INSERT INTO Produccion (id_produccion, fecha_inicio_produccion, cantidad_producida,
    costo_mano_obra, costo_total_materia_prima, costo_iva, costo_total_produccion,
    fecha_fin_produccion, estado_produccion, id_empleado_fk_produccion,id_pedido_fk_produccion)
  VALUES (insrt_id_produccion, insrt_fecha_inicio_produccion, insrt_cantidad_producida,
    insrt_costo_mano_obra, insrt_costo_total_materia_prima, insrt_costo_iva,
    insrt_costo_total_produccion, insrt_fecha_fin_produccion, insrt_estado_produccion,
    insrt_id_empleado_fk_produccion, insrt_id_pedido_fk_produccion);
END$$




CREATE PROCEDURE insrt_Producto_terminado(
  IN insrt_id_producto_t INT,
  IN insrt_nombre_producto_t VARCHAR(50),
  IN insrt_descripcion_producto_t VARCHAR(200),
  IN insrt_categoria_produ_t VARCHAR(50),
  IN insrt_unidad_medida VARCHAR(50),
  IN insrt_estado_producto_t VARCHAR(50),
  IN insrt_id_produccion_fk_producto_terminado INT
)
BEGIN
  INSERT INTO Producto_terminado (id_producto_t, nombre_producto_t, descripcion_producto_t,
    categoria_produ_t, unidad_medida, estado_producto_t, id_produccion_fk_producto_terminado)
  VALUES (insrt_id_producto_t, insrt_nombre_producto_t, insrt_descripcion_producto_t,
    insrt_categoria_produ_t, insrt_unidad_medida, insrt_estado_producto_t,
    insrt_id_produccion_fk_producto_terminado);
END$$


CREATE PROCEDURE insrt_detalle_facturav_produtot(
  IN insrt_id_dettallef_p INT,
  IN insrt_cod_factura_v_fk_detalle INT,
  IN insrt_id_producto_t_fk_detalle INT,
  IN insrt_descripcion VARCHAR(200)
)
BEGIN
  INSERT INTO detalle_facturav_produtot (id_dettallef_p, cod_factura_v_fk_detalle,
    id_producto_t_fk_detalle, descripcion)
  VALUES (insrt_id_dettallef_p, insrt_cod_factura_v_fk_detalle,
    insrt_id_producto_t_fk_detalle, insrt_descripcion);
END$$


CREATE PROCEDURE insrt_Materia_prima(
  IN insrt_id_materia_p INT,
  IN insrt_nom_materia_p VARCHAR(50),
  IN insrt_color_materia_p VARCHAR(50),
  IN insrt_categoria_mp VARCHAR(50),
  IN insrt_tipo_material_materia_p VARCHAR(100),
  IN insrt_stock_actual_materia_p NUMERIC,
  IN insrt_stock_minimo_materia_p NUMERIC,
  IN insrt_descripcion_materia_p VARCHAR(200),
  IN insrt_estado_materia_p VARCHAR(50)
)
BEGIN
  INSERT INTO Materia_prima (id_materia_p, nom_materia_p, color_materia_p, categoria_mp,
    tipo_material_materia_p, stock_actual_materia_p, stock_minimo_materia_p,
    descripcion_materia_p, estado_materia_p)
  VALUES (insrt_id_materia_p, insrt_nom_materia_p, insrt_color_materia_p, insrt_categoria_mp,
    insrt_tipo_material_materia_p, insrt_stock_actual_materia_p, insrt_stock_minimo_materia_p,
    insrt_descripcion_materia_p, insrt_estado_materia_p);
END$$


CREATE PROCEDURE insrt_Factura_compra(
  IN insrt_cod_factura_compra INT,
  IN insrt_fecha_factura_compra DATE,
  IN insrt_total_faactura_compra BIGINT,
  IN insrt_metododepago_factura_compra BIGINT,
  IN insrt_estado_factura_compra VARCHAR(50),
  IN insrt_id_empleado_fk_factura_compra INT
)
BEGIN
  INSERT INTO Factura_compra (cod_factura_compra, fecha_factura_compra,
    total_faactura_compra, metododepago_factura_compra,
    estado_factura_compra, id_empleado_fk_factura_compra)
  VALUES (insrt_cod_factura_compra, insrt_fecha_factura_compra,
    insrt_total_faactura_compra, insrt_metododepago_factura_compra,
    insrt_estado_factura_compra, insrt_id_empleado_fk_factura_compra);
END$$


CREATE PROCEDURE insrt_Detalle_factuc_compra_m(
  IN insrt_id_detalle_fcm INT,
  IN insrt_cod_factura_compra_fk_detalle_fcm INT,
  IN insrt_id_materia_p_compra_fk_detalle_fcm INT,
  IN insrt_cantidad_detalle_factu_fcm NUMERIC,
  IN insrt_descrion_factu_fcm VARCHAR(200)
)
BEGIN
  INSERT INTO Detalle_factuc_compra_m (id_detalle_fcm, cod_factura_compra_fk_detalle_fcm,
    id_materia_p_compra_fk_detalle_fcm, cantidad_detalle_factu_fcm, descrion_factu_fcm)
  VALUES (insrt_id_detalle_fcm, insrt_cod_factura_compra_fk_detalle_fcm,
    insrt_id_materia_p_compra_fk_detalle_fcm, insrt_cantidad_detalle_factu_fcm,
    insrt_descrion_factu_fcm);
END$$


CREATE PROCEDURE insrt_Detalle_produccion_materiap_(
  IN insrt_id_dettalle_produccion_materiap INT,
  IN insrt_id_materia_p_fk_detalle_p_m INT,
  IN insrt_id_produccion_fk_detalle_p_m INT,
  IN insrt_descripcion VARCHAR(200)
)
BEGIN
  INSERT INTO Detalle_produccion_materiap_ (id_dettalle_produccion_materiap,
    id_materia_p_fk_detalle_p_m, id_produccion_fk_detalle_p_m, descripcion)
  VALUES (insrt_id_dettalle_produccion_materiap,
    insrt_id_materia_p_fk_detalle_p_m, insrt_id_produccion_fk_detalle_p_m, insrt_descripcion);
END$$

DELIMITER $$
CREATE PROCEDURE Consultar_producto_t()
BEGIN
    SELECT * FROM Producto_terminado;
END$$

DELIMITER ;
