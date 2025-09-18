use LUXI_FASHON;

--  Consultar todos los empleados con su rol
SELECT E.id_empleado, E.nom_empleado, E.direccion_empleado, E.telefono_empleado, E.correo_empleado, R.nombre_rol
FROM Empleado E
JOIN Rol R ON E.id_rol_fk_empleado = R.id_rol;

--  Consultar todos los clientes con su rol
SELECT C.id_cliente, C.nom_cliente, C.direccion_cliente, C.telefono_cliente, C.correo_cliente, R.nombre_rol
FROM Cliente C
JOIN Rol R ON C.id_rol_fk_cliente = R.id_rol;

-- . Consultar todos los productos terminados con su producción asociada
SELECT P.id_producto_t, P.nombre_producto_t, P.descripcion_producto_t, P.categoria_produ_t, P.estado_producto_t, Pr.id_produccion, Pr.fecha_inicio_produccion
FROM Producto_terminado P
JOIN Produccion Pr ON P.id_produccion_fk_producto_terminado = Pr.id_produccion;

-- . Consultar todos los pedidos con los detalles del cliente y la producción asociada
SELECT Pe.id_pedido, Pe.nom_p_edido, Pe.talla_p_pedido, Pe.color_p_pedido, Pe.categoria_p_pedido, Pe.estado_pedido, C.nom_cliente, Pr.fecha_inicio_produccion
FROM Pedido Pe
JOIN Cliente C ON Pe.id_cliente_fk_pedido = C.id_cliente
JOIN Produccion Pr ON Pe.id_produccion_fk_pedido = Pr.id_produccion;

--  Consultar todas las facturas de venta con los detalles del empleado asociado
SELECT F.cod_factura_v, F.fecha_factura_v, F.sub_total_factura_v, F.iva_factura_v, F.total_factura_v, E.nom_empleado
FROM Factura_Venta F
JOIN Empleado E ON F.id_empleado_fk_factura = E.id_empleado;

--  Consultar todas las facturas de compra con los detalles del empleado asociado
SELECT Fc.cod_factura_compra, Fc.fecha_factura_compra, Fc.total_faactura_compra, E.nom_empleado
FROM Factura_compra Fc
JOIN Empleado E ON Fc.id_empleado_fk_factura_compra = E.id_empleado;

--  Consultar los pedidos junto con los productos terminados y los detalles de la factura de venta
SELECT P.id_pedido, P.nom_p_edido, P.talla_p_pedido, P.color_p_pedido, P.categoria_p_pedido, F.cod_factura_v, D.descripcion
FROM Pedido P
JOIN detalle_facturav_produtot D ON P.id_pedido = D.id_producto_t_fk_detalle
JOIN Factura_Venta F ON D.cod_factura_v_fk_detalle = F.cod_factura_v;

--  Consultar las materias primas junto con sus detalles en las facturas de compra
SELECT Mp.id_materia_p, Mp.nom_materia_p, Mp.color_materia_p, Mp.categoria_mp, Fc.cod_factura_compra, D.cantidad_detalle_factu_fcm
FROM Materia_prima Mp
JOIN Detalle_factuc_compra_m D ON Mp.id_materia_p = D.id_materia_p_compra_fk_detalle_fcm
JOIN Factura_compra Fc ON D.cod_factura_compra_fk_detalle_fcm = Fc.cod_factura_compra;

--  Consultar las producciones junto con los empleados asociados
SELECT Pr.id_produccion, Pr.fecha_inicio_produccion, Pr.fecha_fin_produccion, Pr.estado_produccion, E.nom_empleado
FROM Produccion Pr
JOIN Empleado E ON Pr.id_empleado_fk_produccion = E.id_empleado;

--  Consultar los productos terminados junto con su producción y los detalles de la materia prima utilizada
SELECT P.id_producto_t, P.nombre_producto_t, P.categoria_produ_t, Pr.fecha_inicio_produccion, Mp.nom_materia_p, D.descripcion
FROM Producto_terminado P
JOIN Produccion Pr ON P.id_produccion_fk_producto_terminado = Pr.id_produccion
JOIN Detalle_produccion_materiap_ D ON Pr.id_produccion = D.id_produccion_fk_detalle_p_m
JOIN Materia_prima Mp ON D.id_materia_p_fk_detalle_p_m = Mp.id_materia_p;

--  Consultar los pedidos junto con las materias primas utilizadas y la producción asociada
SELECT Pe.id_pedido, Pe.nom_p_edido, Pe.categoria_p_pedido, Mp.nom_materia_p, Pr.fecha_inicio_produccion
FROM Pedido Pe
JOIN Produccion Pr ON Pe.id_produccion_fk_pedido = Pr.id_produccion
JOIN Detalle_produccion_materiap_ D ON Pr.id_produccion = D.id_produccion_fk_detalle_p_m
JOIN Materia_prima Mp ON D.id_materia_p_fk_detalle_p_m = Mp.id_materia_p;

-- . Consultar los productos terminados junto con los pedidos asociados
SELECT P.id_producto_t, P.nombre_producto_t, P.categoria_produ_t, Pe.nom_p_edido, Pe.fecha_pedido
FROM Producto_terminado P
JOIN Pedido Pe ON P.id_produccion_fk_producto_terminado = Pe.id_produccion_fk_pedido;
