USE LUXI_FASHON;


DELIMITER //
CREATE PROCEDURE consultar_Rol(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM rol;
    ELSE
        SELECT * FROM rol 
        WHERE nombre_rol LIKE CONCAT('%', filtro, '%')
        OR estado = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Empleado(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM empleado;
    ELSE
        SELECT * 
        FROM empleado
        WHERE nom_empleado LIKE CONCAT('%', filtro, '%')
           OR Estado_empleado = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Cliente(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM Cliente;
    ELSE
        SELECT * FROM Cliente
        WHERE nom_cliente LIKE CONCAT('%', filtro, '%')
           OR telefono_cliente = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Factura_Venta(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM factura_venta;
    ELSE
        SELECT * FROM factura_venta
        WHERE fecha_factura_v LIKE CONCAT('%', filtro, '%')
           OR metodo_pago = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Produccion(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM produccion;
    ELSE
        SELECT * FROM produccion
        WHERE fecha_inicio_produccion LIKE CONCAT('%', filtro, '%')
           OR fecha_fin_produccion = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Pedido(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM pedido;
    ELSE
        SELECT * FROM pedido
        WHERE fecha_pedido LIKE CONCAT('%', filtro, '%')
           OR categoria_p_pedido = filtro
            OR nom_p_edido = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Producto_terminado(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM producto_terminado;
    ELSE
        SELECT * FROM producto_terminado
        WHERE nombre_producto_t LIKE CONCAT('%', filtro, '%')
           OR categoria_produ_t = filtro;
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE consultar_detalle_facturav_produtot()
BEGIN
  SELECT * FROM detalle_facturav_produtot;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Materia_prima(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM materia_prima;
    ELSE
        SELECT * FROM materia_prima
        WHERE nom_materia_p LIKE CONCAT('%', filtro, '%')
           OR categoria_mp = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Factura_compra(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN
        SELECT * FROM factura_compra;
    ELSE
        SELECT * FROM factura_compra
        WHERE fecha_factura_compra LIKE CONCAT('%', filtro, '%')
           OR estado_factura_compra = filtro;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Detalle_factuc_compra_m()
BEGIN
  SELECT * FROM detalle_factuc_compra_m;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE consultar_Detalle_produccion_materiap()
BEGIN
  SELECT * FROM detalle_produccion_materiap_;
END //

DELIMITER ;