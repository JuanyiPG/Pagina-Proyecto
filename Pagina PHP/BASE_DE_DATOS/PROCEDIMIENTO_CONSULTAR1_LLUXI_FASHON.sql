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

END//

CREATE  PROCEDURE consultar_Empleado(IN filtro VARCHAR(100))
BEGIN
    IF filtro IS NULL OR filtro = '' THEN 
	SELECT *  FROM empleado; 
    ELSE
    SELECT * FROM empleado 
    WHERE nom_empleado LIKE concat('%', filtro ,'%')
    OR Estado_emplado = filtro; 
    END IF; 
END //


CREATE PROCEDURE consultar_Cliente(IN filtro VARCHAR(100))
BEGIN
  IF filtro IS NULL OR filtro = '' THEN 
  SELECT * FROM cliente;
  ELSE 
  SELECT * FROM cliente 
  WHERE nom_cliente LIKE concat('%',filtro,'%')
  OR telefono_cliente = filtro; 
  END IF; 
END //


CREATE PROCEDURE consultar_Factura_Venta(IN filtro VARCHAR(100))
BEGIN
IF filtro IS NULL OR filtro = '' THEN 
  SELECT * FROM factura_venta;
  ELSE 
  SELECT * FROM factura_venta
  WHERE fecha_factura_v LIKE concat('%', filtro, '%');
  END IF; 
END //


CREATE PROCEDURE consultar_Produccion(IN filtro VARCHAR(100))
BEGIN
IF filtro IS NULL OR filtro = '' THEN
  SELECT * FROM Produccion;
  ELSE 
  SELECT * FROM Produccion
  WHERE fecha_inicio_produccion LIKE concat('%', filtro, '%');
  END IF; 
END //


CREATE PROCEDURE consultar_Pedido(IN filtro VARCHAR(100))
BEGIN
IF filtro IS NULL OR filtro = '' THEN
  SELECT * FROM pedido;
  ELSE 
  SELECT * FROM pedido
  WHERE nom_p_edido LIKE concat('%', filtro, '%')
  OR estado_pedido = filtro; 
  END IF; 
END //


CREATE PROCEDURE consultar_Producto_terminado(IN filtro VARCHAR(100))
BEGIN
IF filtro IS NULL OR filtro = '' THEN 
  SELECT * FROM Producto_terminado;
  ELSE 
  SELECT * FROM producto_terminado 
  WHERE nombre_producto_t LIKE concat('%', filtro, '%')
  OR categoria_produ_t = filtro; 
  END IF;
END //


CREATE PROCEDURE consultar_detalle_facturav_produtot(IN filtro VARCHAR(100))
BEGIN
  SELECT * FROM detalle_facturav_produtot;
END //


CREATE PROCEDURE consultar_Materia_prima(IN filtro VARCHAR(100))
BEGIN
IF filtro IS NULL OR filtro = '' THEN 
  SELECT * FROM materia_prima;
  ELSE 
  SELECT * FROM materia_prima 
  WHERE nom_materia_p LIKE concat('%', filtro, '%')
  OR categoria_mp = filtro; 
  END IF; 
END //


CREATE PROCEDURE consultar_Factura_compra(IN filtro VARCHAR(100))
BEGIN
IF filtro IS NULL OR filtro = '' THEN 
  SELECT * FROM factura_compra;
  ELSE 
  SELECT * FROM factura_compra 
  WHERE fecha_factura_compra LIKE concat('%',filtro,'%')
  OR estado_factura_compra = filtro; 
  END IF; 
END //


CREATE PROCEDURE consultar_Detalle_factuc_compra_m(IN filtro VARCHAR(100))
BEGIN
  SELECT * FROM Detalle_factuc_compra_m;
END //


CREATE PROCEDURE consultar_Detalle_produccion_materiap(IN filtro VARCHAR(100))
BEGIN
  SELECT * FROM Detalle_produccion_materiap_;
END //

DELIMITER ;
