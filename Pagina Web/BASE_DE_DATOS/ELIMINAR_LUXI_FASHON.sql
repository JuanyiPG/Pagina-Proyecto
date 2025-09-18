use LUXI_FASHON;

DELIMITER //
CREATE PROCEDURE ELIMINAR_PRODUCTO_T (IN id_producto INT)
BEGIN
    DELETE FROM detalle_facturav_produtot WHERE id_producto_t_fk_detalle = id_producto;
    DELETE FROM Producto_terminado WHERE id_producto_t = id_producto;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_CLIENTE (IN id_cliente INT)
BEGIN
    DELETE FROM Pedido WHERE id_cliente_fk_pedido = id_cliente;
    DELETE FROM Cliente WHERE id_cliente = id_cliente;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_EMPLEADO (IN id_empleado INT)
BEGIN
    DELETE FROM Factura_Venta WHERE id_empleado_fk_factura = id_empleado;
    DELETE FROM Factura_compra WHERE id_empleado_fk_factura_compra = id_empleado;
    DELETE FROM Produccion WHERE id_empleado_fk_produccion = id_empleado;
    DELETE FROM Empleado WHERE id_empleado = id_empleado;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_FACTURA_COMPRA (IN cod_factura INT)
BEGIN
    DELETE FROM Detalle_factuc_compra_m WHERE cod_factura_compra_fk_detalle_fcm = cod_factura;
    DELETE FROM Factura_compra WHERE cod_factura_compra = cod_factura;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_FACTURA_VENTA (IN cod_factura INT)
BEGIN
    DELETE FROM detalle_facturav_produtot WHERE cod_factura_v_fk_detalle = cod_factura;
    DELETE FROM Factura_Venta WHERE cod_factura_v = cod_factura;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_MATERIA_PRIMA (IN id_materia INT)
BEGIN
    DELETE FROM Detalle_factuc_compra_m WHERE id_materia_p_compra_fk_detalle_fcm = id_materia;
    DELETE FROM Detalle_produccion_materiap_ WHERE id_materia_p_fk_detalle_p_m = id_materia;
    DELETE FROM Materia_prima WHERE id_materia_p = id_materia;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_PRODUCCION (IN id_produccion INT)
BEGIN
    DELETE FROM Pedido WHERE id_produccion_fk_pedido = id_produccion;
    DELETE FROM Producto_terminado WHERE id_produccion_fk_producto_terminado = id_produccion;
    DELETE FROM Detalle_produccion_materiap_ WHERE id_produccion_fk_detalle_p_m = id_produccion;
    DELETE FROM Produccion WHERE id_produccion = id_produccion;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_PEDIDO (IN id_pedido INT)
BEGIN
    DELETE FROM detalle_facturav_produtot WHERE cod_factura_v_fk_detalle IN 
        (SELECT cod_factura_v_fk_detalle FROM Factura_Venta WHERE cod_factura_v_fk_detalle = id_pedido);
    DELETE FROM Pedido WHERE id_pedido = id_pedido;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_ROL (IN id_rol INT)
BEGIN
    DELETE FROM Empleado WHERE id_rol_fk_empleado = id_rol;
    DELETE FROM Cliente WHERE id_rol_fk_cliente = id_rol;
    DELETE FROM Rol WHERE id_rol = id_rol;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_DETALLE_PRODUCCION_MATERIA (IN id_detalle INT)
BEGIN
    DELETE FROM Detalle_produccion_materiap_ WHERE id_dettalle_produccion_materiap = id_detalle;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_DETALLE_FACTURA_COMPRA (IN id_detalle INT)
BEGIN
    DELETE FROM Detalle_factuc_compra_m WHERE id_detalle_fcm = id_detalle;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ELIMINAR_DETALLE_FACTURA_VENTA (IN id_detalle INT)
BEGIN
    DELETE FROM detalle_facturav_produtot WHERE id_dettallef_p = id_detalle;
END //
DELIMITER ;
