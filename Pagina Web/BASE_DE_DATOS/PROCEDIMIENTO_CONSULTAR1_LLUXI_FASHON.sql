USE LUXI_FASHON;

DELIMITER //


CREATE   PROCEDURE consultar_Rol()
BEGIN
  SELECT * FROM Rol;
END //


CREATE  PROCEDURE consultar_Empleado()
BEGIN
  SELECT * FROM Empleado;
END //


CREATE PROCEDURE consultar_Cliente()
BEGIN
  SELECT * FROM Cliente;
END //


CREATE PROCEDURE consultar_Factura_Venta()
BEGIN
  SELECT * FROM Factura_Venta;
END //


CREATE PROCEDURE consultar_Produccion()
BEGIN
  SELECT * FROM Produccion;
END //


CREATE PROCEDURE consultar_Pedido()
BEGIN
  SELECT * FROM Pedido;
END //


CREATE PROCEDURE consultar_Producto_terminado()
BEGIN
  SELECT * FROM Producto_terminado;
END //


CREATE PROCEDURE consultar_detalle_facturav_produtot()
BEGIN
  SELECT * FROM detalle_facturav_produtot;
END //


CREATE PROCEDURE consultar_Materia_prima()
BEGIN
  SELECT * FROM Materia_prima;
END //


CREATE PROCEDURE consultar_Factura_compra()
BEGIN
  SELECT * FROM Factura_compra;
END //


CREATE PROCEDURE consultar_Detalle_factuc_compra_m()
BEGIN
  SELECT * FROM Detalle_factuc_compra_m;
END //


CREATE PROCEDURE consultar_Detalle_produccion_materiap()
BEGIN
  SELECT * FROM Detalle_produccion_materiap_;
END //

DELIMITER ;
