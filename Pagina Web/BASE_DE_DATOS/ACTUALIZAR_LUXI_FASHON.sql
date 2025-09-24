USE LUXI_FASHON;

DELIMITER $$


CREATE PROCEDURE actualizar_Rol (
    IN actuali_id_rol INT,
    IN actuali_nombre_rol VARCHAR(50),
    IN actuali_descripcion VARCHAR(200),
    IN actuali_estado VARCHAR(50)
)
BEGIN
    UPDATE Rol
    SET nombre_rol = actuali_nombre_rol,
        descripcion = actuali_descripcion,
        estado = actuali_estado
    WHERE id_rol = actuali_id_rol;
END$$

CREATE PROCEDURE actualizar_Empleado (
    IN actuali_id_empleado INT,
    IN actuali_nom_empleado VARCHAR(50),
    IN actuali_direccion_empleado VARCHAR(100),
    IN actuali_tipo_sangre VARCHAR(20),
    IN actuali_telefono_empleado INT,
    IN actuali_correo_empleado VARCHAR(100),
    IN actuali_fecha_ing_empleado DATE,
    IN actuali_salario_empleado FLOAT,
    IN actuali_estado_empleado VARCHAR(50),
    IN actuali_id_rol_fk_empleado INT
)
BEGIN
    UPDATE Empleado
    SET nom_empleado = actuali_nom_empleado,
        direccion_empleado = actuali_direccion_empleado,
        tipo_sangre = actuali_tipo_sangre,
        telefono_empleado = actuali_telefono_empleado,
        correo_empleado = actuali_correo_empleado,
        Fecha_ing_empleado = actuali_fecha_ing_empleado,
        salario_empleado = actuali_salario_empleado,
        Estado_empleado = actuali_estado_empleado,
        id_rol_fk_empleado = actuali_id_rol_fk_empleado
    WHERE id_empleado = actuali_id_empleado;
END$$


CREATE PROCEDURE actualizar_Cliente (
    IN actuali_id_cliente INT,
    IN actuali_nom_cliente VARCHAR(50),
    IN actuali_direccion_cliente VARCHAR(100),
    IN actuali_telefono_cliente INT,
    IN actuali_correo_cliente VARCHAR(100),
    IN actuali_id_rol_fk_cliente INT
)
BEGIN
    UPDATE Cliente
    SET nom_cliente = actuali_nom_cliente,
        direccion_cliente = actuali_direccion_cliente,
        telefono_cliente = actuali_telefono_cliente,
        correo_cliente = actuali_correo_cliente,
        id_rol_fk_cliente = actuali_id_rol_fk_cliente
    WHERE id_cliente = actuali_id_cliente;
END$$


CREATE PROCEDURE actualizar_Factura_Venta (
    IN actuali_cod_factura_v INT,
    IN actuali_fecha_factura_v DATE,
    IN actuali_sub_total_factura_v BIGINT,
    IN actuali_iva_factura_v BIGINT,
    IN actuali_total_factura_v BIGINT,
    IN actuali_metodo_pago VARCHAR(50),
    IN actuali_descuento INT,
    IN actuali_estado_factura_venta VARCHAR(50),
    IN actuali_id_empleado_fk_factura INT
)
BEGIN
    UPDATE Factura_Venta
    SET fecha_factura_v = actuali_fecha_factura_v,
        sub_total_factura_v = actuali_sub_total_factura_v,
        iva_factura_v = actuali_iva_factura_v,
        total_factura_v = actuali_total_factura_v,
        metodo_pago = actuali_metodo_pago,
        descuento = actuali_descuento,
        estado_factura_venta = actuali_estado_factura_venta,
        id_empleado_fk_factura = actuali_id_empleado_fk_factura
    WHERE cod_factura_v = actuali_cod_factura_v;
END$$


CREATE PROCEDURE actualizar_Produccion (
    IN actuali_id_produccion INT,
    IN actuali_fecha_inicio_produccion DATE,
    IN actuali_cantidad_producida NUMERIC,
    IN actuali_costo_mano_obra BIGINT,
    IN actuali_costo_total_materia_prima BIGINT,
    IN costo_iva BIGINT,
    IN actuali_costo_total_produccion BIGINT,
    IN actuali_fecha_fin_produccion DATE,
    IN actuali_estado_produccion VARCHAR(50),
    IN actuali_id_empleado_fk_produccion INT
)
BEGIN
    UPDATE Produccion
    SET fecha_inicio_produccion = actuali_fecha_inicio_produccion,
        cantidad_producida = actuali_cantidad_producida,
        costo_mano_obra = actuali_costo_mano_obra,
        costo_total_materia_prima = actuali_costo_total_materia_prima,
        costo_iva = actuali_costo_iva,
        costo_total_produccion = actuali_costo_total_produccion,
        fecha_fin_produccion = actuali_fecha_fin_produccion,
        estado_produccion = actuali_estado_produccion,
        id_empleado_fk_produccion = actuali_id_empleado_fk_produccion
    WHERE id_produccion = actuali_id_produccion;
END$$


CREATE PROCEDURE actualizar_Pedido (
    IN actuali_id_pedido INT,
    IN actuali_nom_p_edido VARCHAR(100),
    IN actuali_talla_p_pedido VARCHAR(50),
    IN actuali_color_p_pedido VARCHAR(50),
    IN actuali_categoria_p_pedido VARCHAR(50),
    IN actuali_material_p_pedido VARCHAR(100),
    IN actuali_cant_producto NUMERIC,
    IN actuali_descripcion_p_pedido VARCHAR(200),
    IN actuali_fecha_pedido DATE,
    IN actuali_sub_total_pedido BIGINT,
    IN actuali_valor_pedido BIGINT,
    IN actuali_estado_pedido VARCHAR(50),
    IN actuali_id_cliente_fk_pedido INT,
    IN actuali_id_produccion_fk_pedido INT
)
BEGIN
    UPDATE Pedido
    SET nom_p_edido = actuali_nom_p_edido,
        talla_p_pedido = actuali_talla_p_pedido,
        color_p_pedido = actuali_color_p_pedido,
        categoria_p_pedido = actuali_categoria_p_pedido,
        material_p_pedido = actuali_material_p_pedido,
        cant_producto = actuali_cant_producto,
        descripcion_p_pedido = actuali_descripcion_p_pedido,
        fecha_pedido = actuali_fecha_pedido,
        sub_total_pedido = actuali_sub_total_pedido,
        valor_pedido = actuali_valor_pedido,
        estado_pedido = actuali_estado_pedido,
        id_cliente_fk_pedido = actuali_id_cliente_fk_pedido,
        id_produccion_fk_pedido = actuali_id_produccion_fk_pedido
    WHERE id_pedido = actuali_id_pedido;
END$$


CREATE PROCEDURE actualizar_Producto_terminado (
    IN actuali_id_producto_t INT,
    IN actuali_nombre_producto_t VARCHAR(50),
    IN actuali_descripcion_producto_t VARCHAR(200),
    IN actuali_categoria_produ_t VARCHAR(50),
    IN actuali_unidad_medida VARCHAR(50),
    IN actuali_estado_producto_t VARCHAR(50),
    IN actuali_id_produccion_fk_producto_terminado INT
)
BEGIN
    UPDATE Producto_terminado
    SET nombre_producto_t = actuali_nombre_producto_t,
        descripcion_producto_t = actuali_descripcion_producto_t,
        categoria_produ_t = actuali_categoria_produ_t,
        unidad_medida = actuali_unidad_medida,
        estado_producto_t = actuali_estado_producto_t,
        id_produccion_fk_producto_terminado = actuali_id_produccion_fk_producto_terminado
    WHERE id_producto_t = actuali_id_producto_t;
END$$


CREATE PROCEDURE actualizar_detalle_facturav_produtot (
    IN actuali_id_dettallef_p INT,
    IN actuali_cod_factura_v_fk_detalle INT,
    IN actuali_id_producto_t_fk_detalle INT,
    IN actuali_descripcion VARCHAR(200)
)
BEGIN
    UPDATE detalle_facturav_produtot
    SET cod_factura_v_fk_detalle = actuali_cod_factura_v_fk_detalle,
        id_producto_t_fk_detalle = actuali_id_producto_t_fk_detalle,
        descripcion = actuali_descripcion
    WHERE id_dettallef_p = actuali_id_dettallef_p;
END$$


CREATE PROCEDURE actualizar_Materia_prima (
    IN actuali_id_materia_p INT,
    IN actuali_nom_materia_p VARCHAR(50),
    IN actuali_color_materia_p VARCHAR(50),
    IN actuali_categoria_mp VARCHAR(50),
    IN actuali_tipo_material_materia_p VARCHAR(100),
    IN actuali_stock_actual_materia_p NUMERIC,
    IN actuali_stock_minimo_materia_p NUMERIC,
    IN actuali_descripcion_materia_p VARCHAR(200),
    IN actuali_estado_materia_p VARCHAR(50)
)
BEGIN
    UPDATE Materia_prima
    SET nom_materia_p = actuali_nom_materia_p,
        color_materia_p = actuali_color_materia_p,
        categoria_mp = actuali_categoria_mp,
        tipo_material_materia_p = actuali_tipo_material_materia_p,
        stock_actual_materia_p = actuali_stock_actual_materia_p,
        stock_minimo_materia_p = actuali_stock_minimo_materia_p,
        descripcion_materia_p = actuali_descripcion_materia_p,
        estado_materia_p = actuali_estado_materia_p
    WHERE id_materia_p = actuali_id_materia_p;
END$$


CREATE PROCEDURE actualizar_Factura_compra (
    IN actuali_cod_factura_compra INT,
    IN actuali_fecha_factura_compra DATE,
    IN actuali_total_faactura_compra BIGINT,
    IN actuali_metododepago_factura_compra VARCHAR(50),
    IN actuali_estado_factura_compra VARCHAR(50),
    IN actuali_id_empleado_fk_factura_compra INT
)
BEGIN
    UPDATE Factura_compra
    SET fecha_factura_compra = actuali_fecha_factura_compra,
        total_faactura_compra = actuali_total_faactura_compra,
        metododepago_factura_compra = actuali_metododepago_factura_compra,
        estado_factura_compra = actuali_estado_factura_compra,
        id_empleado_fk_factura_compra = actuali_id_empleado_fk_factura_compra
    WHERE cod_factura_compra = actuali_cod_factura_compra;
END$$


CREATE PROCEDURE actualizar_Detalle_factuc_compra_m (
    IN actuali_id_detalle_fcm INT,
    IN actuali_cod_factura_compra_fk_detalle_fcm INT,
    IN actuali_id_materia_p_compra_fk_detalle_fcm INT,
    IN actuali_cantidad_detalle_factu_fcm NUMERIC,
    IN actuali_descrion_factu_fcm VARCHAR(200)
)
BEGIN
    UPDATE Detalle_factuc_compra_m
    SET cod_factura_compra_fk_detalle_fcm = actuali_cod_factura_compra_fk_detalle_fcm,
        id_materia_p_compra_fk_detalle_fcm = actuali_id_materia_p_compra_fk_detalle_fcm,
        cantidad_detalle_factu_fcm = actuali_cantidad_detalle_factu_fcm,
        descrion_factu_fcm = actuali_descrion_factu_fcm
    WHERE id_detalle_fcm = actuali_id_detalle_fcm;
END$$


CREATE PROCEDURE actualizar_Detalle_produccion_materiap (
    IN actuali_id_dettalle_produccion_materiap INT,
    IN actuali_id_materia_p_fk_detalle_p_m INT,
    IN actuali_id_produccion_fk_detalle_p_m INT,
    IN actuali_descripcion VARCHAR(200)
)
BEGIN
    UPDATE Detalle_produccion_materiap_
    SET id_materia_p_fk_detalle_p_m = actuali_id_materia_p_fk_detalle_p_m,
        id_produccion_fk_detalle_p_m = actuali_id_produccion_fk_detalle_p_m,
        descripcion = actuali_descripcion
    WHERE id_dettalle_produccion_materiap = actuali_id_dettalle_produccion_materiap;
END$$

DELIMITER ;
