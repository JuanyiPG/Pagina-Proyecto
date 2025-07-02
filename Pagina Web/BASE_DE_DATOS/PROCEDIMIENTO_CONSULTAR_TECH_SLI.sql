USE TECH_SLY ;

DELIMITER $$
CREATE PROCEDURE consultar_Empleado()
BEGIN
    SELECT * FROM Empleado;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Telef_empleado()
BEGIN
    SELECT * FROM Telef_empleado;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Correo_emple()
BEGIN
    SELECT * FROM Correo_emple;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Cliente()
BEGIN
    SELECT * FROM Cliente;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Telef_clien()
BEGIN
    SELECT * FROM Telef_clien;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_correo_client()
BEGIN
    SELECT * FROM correo_client;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Usuarios()
BEGIN
    SELECT * FROM Usuarios;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Usuari_emple()
BEGIN
    SELECT * FROM Usuari_emple;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_usuari_cliente()
BEGIN
    SELECT * FROM usuari_cliente;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Facturacion()
BEGIN
    SELECT * FROM Facturacion;
END$$


DELIMITER $$
CREATE PROCEDURE consultar_Producto()
BEGIN
    SELECT * FROM Producto;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Materia_prima()
BEGIN
    SELECT * FROM Materia_prima;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Producto_MateriaPrima()
BEGIN
    SELECT * FROM Producto_MateriaPrima;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Compra_materia_prima()
BEGIN
    SELECT * FROM Compra_materia_prima;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Pedido()
BEGIN
    SELECT * FROM Pedido;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Produccion()
BEGIN
    SELECT * FROM Produccion;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_Metododepago()
BEGIN
    SELECT * FROM Metododepago;
END$$

DELIMITER $$
CREATE PROCEDURE consultar_descrip_detalle()
BEGIN
    SELECT * FROM descrip_detalle;
END$$
