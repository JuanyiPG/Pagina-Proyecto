USE TECH_SLY ;

SELECT 
    Empleado.Id_emple AS ID_Empleado,
    Empleado.Nom_emple AS Nombre_Empleado,
    Empleado.salario_emple AS Salario,
    Telef_empleado.telef_emple_1 AS Telefono,
    Correo_emple.correo_emple_1 AS Correo
FROM Empleado
LEFT JOIN Telef_empleado ON Empleado.Id_emple = Telef_empleado.Id_emple_fk_telef_emple
LEFT JOIN Correo_emple ON Empleado.Id_emple = Correo_emple.Id_emple_fk_correo_emple
WHERE Empleado.estado_emple = TRUE;


SELECT 
    Cliente.Id_cliente AS ID_Cliente,
    Cliente.Nom_cliente AS Nombre_Cliente,
    Cliente.ciudad_cliente AS Ciudad,
    Telef_clien.telf_cliente_1 AS Telefono,
    correo_client.correo_client_1 AS Correo
FROM Cliente
LEFT JOIN Telef_clien ON Cliente.Id_cliente = Telef_clien.Id_cliente_fk_telef_cliente
LEFT JOIN correo_client ON Cliente.Id_cliente = correo_client.Id_cliente_fk_correo_client
WHERE Cliente.estado_cliente = TRUE;

SELECT 
    Pedido.Id_pedido AS Codigo_Pedido,
    Cliente.Nom_cliente AS Nombre_Cliente,
    Producto.Nom_produc AS Nombre_Producto,
    descrip_detalle.cantidad AS Cantidad,
    descrip_detalle.Precio_unitario AS Precio_Unitario,
    descrip_detalle.sub_total AS Subtotal
FROM descrip_detalle
JOIN Pedido ON descrip_detalle.Id_pedido_fk_descrip_detalle = Pedido.Id_pedido
JOIN Cliente ON Pedido.Id_cliente_fk_pedido = Cliente.Id_cliente
JOIN Producto ON descrip_detalle.Cod_produc_fk_descrip_detalle = Producto.Cod_produc
WHERE Pedido.Estado_pedido = 'Enviado';


SELECT 
    Id_materia AS ID_Materia,
    Nom_materia_prima AS Nombre_Materia,
    Stock_actual,
    Stock_minimo
FROM Materia_prima
WHERE Stock_actual < Stock_minimo
  AND estado_materia = TRUE;


SELECT 
    Produccion.Id_produccion AS Codigo_Produccion,
    Producto.Nom_produc AS Producto,
    Produccion.Fecha_ini_producc AS Fecha_Inicio,
    Produccion.cantidad_producida AS Cantidad,
    Produccion.Estado_produccion AS Estado
FROM Produccion
JOIN Producto ON Produccion.Id_producto_fk_produccion = Producto.Cod_produc
WHERE Produccion.Estado_produccion = 'En proceso';



SELECT 
    Produccion.Id_produccion AS Codigo_Produccion,
    Producto.Nom_produc AS Producto,
    Produccion.Fecha_ini_producc AS Fecha_Inicio,
    Produccion.cantidad_producida AS Cantidad,
    Produccion.Estado_produccion AS Estado
FROM Produccion
JOIN Producto ON Produccion.Id_producto_fk_produccion = Producto.Cod_produc
WHERE Produccion.Estado_produccion = 'En proceso';

