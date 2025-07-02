USE TECH_SLY ;

DELIMITER $$

CREATE PROCEDURE actualizar_Empleado (
    IN actuali_Id_emple BIGINT,
    IN actuali_Nom_emple VARCHAR(30),
    IN actuali_fech_ingre_emple DATE,
    IN actuali_RH_emple VARCHAR(5),
    IN actuali_salario_emple NUMERIC,
    IN actuali_fech_naci_emple DATE,
    IN actuali_direc_emple VARCHAR(30),
    IN actuali_estado_emple BOOLEAN
)
BEGIN
    UPDATE Empleado
    SET Nom_emple = actuali_Nom_emple,
        fech_ingre_emple = actuali_fech_ingre_emple,
        RH_emple = actuali_RH_emple,
        salario_emple = actuali_salario_emple,
        fech_naci_emple = actuali_fech_naci_emple,
        direc_emple = actuali_direc_emple,
        estado_emple = actuali_estado_emple
    WHERE Id_emple = actuali_Id_emple;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Telef_empleado (
    IN actuali_Id_telef_emple INT,
    IN actuali_telef_emple_1 NUMERIC,
    IN actuali_Id_emple_fk_telef_emple BIGINT,
    IN actuali_estado_tele_emple BOOLEAN
)
BEGIN
    UPDATE Telef_empleado
    SET telef_emple_1 = actuali_telef_emple_1,
        Id_emple_fk_telef_emple = actuali_Id_emple_fk_telef_emple,
        estado_tele_emple = actuali_estado_tele_emple
    WHERE Id_telef_emple = actuali_Id_telef_emple;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Correo_emple (
    IN actuali_Id_correo_emple INT,
    IN actuali_correo_emple_1 VARCHAR(40),
    IN actuali_Id_emple_fk_correo_emple BIGINT,
    IN actuali_estado_correo_emple BOOLEAN
)
BEGIN
    UPDATE Correo_emple
    SET correo_emple_1 = actuali_correo_emple_1,
        Id_emple_fk_correo_emple = actuali_Id_emple_fk_correo_emple,
        estado_correo_emple = actuali_estado_correo_emple
    WHERE Id_correo_emple = actuali_Id_correo_emple;
END$$


DELIMITER $$
CREATE PROCEDURE actualizar_Cliente (
    IN actuali_Id_cliente BIGINT,
    IN actuali_Nom_cliente VARCHAR(30),
    IN actuali_fecha_naci_clien DATE,
    IN actuali_ciudad_cliente VARCHAR(30),
    IN actuali_estado_cliente BOOLEAN
)
BEGIN
    UPDATE Cliente
    SET Nom_cliente = actuali_Nom_cliente,
        fecha_naci_clien = actuali_fecha_naci_clien,
        ciudad_cliente = actuali_ciudad_cliente,
        estado_cliente = actuali_estado_cliente
    WHERE Id_cliente = actuali_Id_cliente;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Telef_clien (
    IN actuali_Id_telef_cliente INT,
    IN actuali_telf_cliente_1 NUMERIC,
    IN actuali_Id_cliente_fk_telef_cliente BIGINT,
    IN actuali_estado_telef_cliente BOOLEAN
)
BEGIN
    UPDATE Telef_clien
    SET telf_cliente_1 = actuali_telf_cliente_1,
        Id_cliente_fk_telef_cliente = actuali_Id_cliente_fk_telef_cliente,
        estado_telef_cliente = actuali_estado_telef_cliente
    WHERE Id_telef_cliente = actuali_Id_telef_cliente;
END$$

DELIMITER $$S
CREATE PROCEDURE actualizar_correo_client (
    IN actuali_Id_correo_client INT,
    IN actuali_correo_client_1 VARCHAR(40),
    IN actuali_Id_cliente_fk_correo_client BIGINT,
    IN actuali_Estado_correo_client BOOLEAN
)
BEGIN
    UPDATE correo_client
    SET correo_client_1 = actuali_correo_client_1,
        Id_cliente_fk_correo_client = actuali_Id_cliente_fk_correo_client,
        Estado_correo_client = actuali_Estado_correo_client
    WHERE Id_correo_client = actuali_Id_correo_client;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Usuarios (
    IN actuali_Id_usuario INT,
    IN actuali_Nom_usuario VARCHAR(30),
    IN actuali_Contraseña VARCHAR(40),
    IN actuali_estado_usuario BOOLEAN
)
BEGIN
    UPDATE Usuarios
    SET Nom_usuario = actuali_Nom_usuario,
        Contraseña = actuali_Contraseña,
        estado_usuario = actuali_estado_usuario
    WHERE Id_usuario = actuali_Id_usuario;
END$$

DELIMITER $$

CREATE PROCEDURE actualizar_Usuari_emple (
    IN actuali_Id_usu_emple INT,
    IN actuali_Id_emple_fk_usuari_emple BIGINT
)
BEGIN
    UPDATE Usuari_emple
    SET Id_emple_fk_usuari_emple = actuali_Id_emple_fk_usuari_emple
    WHERE Id_usu_emple = actuali_Id_usu_emple;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_usuari_cliente (
    IN actuali_Id_usu_clen INT,
    IN actuali_Id_clien_fk_usuari_cliente BIGINT
)
BEGIN
    UPDATE usuari_cliente
    SET Id_clien_fk_usuari_cliente = actuali_Id_clien_fk_usuari_cliente
    WHERE Id_usu_clen = actuali_Id_usu_clen;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Facturacion (
    IN actuali_Cod_factu INT,
    IN actuali_fecha_factu DATE,
    IN actuali_IVA_factu BIGINT,
    IN actuali_subtotal_factu BIGINT,
    IN actuali_Total_factu BIGINT,
    IN actuali_Id_emple_fk_facturacion BIGINT,
    IN actuali_estado_facturacion BOOLEAN
)
BEGIN
    UPDATE Facturacion
    SET fecha_factu = actuali_fecha_factu,
        IVA_factu = actuali_IVA_factu,
        subtotal_factu = actuali_subtotal_factu,
        Total_factu = actuali_Total_factu,
        Id_emple_fk_facturacion = actuali_Id_emple_fk_facturacion,
        estado_facturacion = actuali_estado_facturacion
    WHERE Cod_factu = actuali_Cod_factu;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Producto (
    IN actuali_Cod_produc INT,
    IN actuali_Nom_produc VARCHAR(30),
    IN actuali_talla_producto VARCHAR(15),
    IN actuali_color_producto VARCHAR(10),
    IN actuali_Categoria_producto VARCHAR(30),
    IN actuali_Materi_produc VARCHAR(30),
    IN actuali_Medida_produc NUMERIC,
    IN actuali_Cant_produc NUMERIC,
    IN actuali_Cant_minima BIGINT,
    IN actuali_valor_produc BIGINT,
    IN actuali_estilo_producto VARCHAR(30),
    IN actuali_descripcion_producto VARCHAR(50),
    IN actuali_estado_produ BOOLEAN
)
BEGIN
    UPDATE Producto
    SET Nom_produc = actuali_Nom_produc,
        talla_producto = actuali_talla_producto,
        color_producto = actuali_color_producto,
        Categoria_producto = actuali_Categoria_producto,
        Materi_produc = actuali_Materi_produc,
        Medida_produc = actuali_Medida_produc,
        Cant_produc = actuali_Cant_produc,
        Cant_minima = actuali_Cant_minima,
        valor_produc = actuali_valor_produc,
        estilo_producto = actuali_estilo_producto,
        descripcion_producto = actuali_descripcion_producto,
        estado_produ = actuali_estado_produ
    WHERE Cod_produc = actuali_Cod_produc;
END$$


DELIMITER $$

CREATE PROCEDURE actualizar_Materia_prima (
    IN actuali_Id_materia INT,
    IN actuali_Nom_materia_prima VARCHAR(40),
    IN actuali_Tipo_material VARCHAR(30),
    IN actuali_Color VARCHAR(30),
    IN actuali_Stock_actual NUMERIC,
    IN actuali_Stock_minimo NUMERIC,
    IN actuali_Descripcion VARCHAR(50),
    IN actuali_estado_materia BOOLEAN,
    IN actuali_Id_producto_fk_materia_prima INT
)
BEGIN
    UPDATE Materia_prima
    SET Nom_materia_prima = actuali_Nom_materia_prima,
        Tipo_material = actuali_Tipo_material,
        Color = actuali_Color,
        Stock_actual = actuali_Stock_actual,
        Stock_minimo = actuali_Stock_minimo,
        Descripcion = actuali_Descripcion,
        estado_materia = actuali_estado_materia,
        Id_producto_fk_materia_prima = actuali_Id_producto_fk_materia_prima
    WHERE Id_materia = actuali_Id_materia;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Producto_MateriaPrima (
    IN actuali_id_prod_materia INT,
    IN actuali_id_producto_fk_prod_materi INT,
    IN actuali_id_materia_fk_prod_materi INT,
    IN actuali_cantidad_utilizada NUMERIC,
    IN actuali_unidad VARCHAR(10)
)
BEGIN
    UPDATE Producto_MateriaPrima
    SET id_producto_fk_prod_materi = actuali_id_producto_fk_prod_materi,
        id_materia_fk_prod_materi = actuali_id_materia_fk_prod_materi,
        cantidad_utilizada = actuali_cantidad_utilizada,
        unidad = actuali_unidad
    WHERE id_prod_materia = actuali_id_prod_materia;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Compra_materia_prima (
    IN actuali_Id_compra_m INT,
    IN actuali_cantidad_compra BIGINT,
    IN actuali_valor_compra BIGINT,
    IN actuali_descrip_compra VARCHAR(50),
    IN actuali_fecha_compra DATE,
    IN actuali_Id_Materiaprima_fk_materia_c INT,
    IN actuali_Estado_compra_m BOOLEAN
)
BEGIN
    UPDATE Compra_materia_prima
    SET cantidad_compra = actuali_cantidad_compra,
        valor_compra = actuali_valor_compra,
        descrip_compra = actuali_descrip_compra,
        fecha_compra = actuali_fecha_compra,
        Id_Materiaprima_fk_materia_c = actuali_Id_Materiaprima_fk_materia_c,
        Estado_compra_m = actuali_Estado_compra_m
    WHERE Id_compra_m = actuali_Id_compra_m;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Pedido (
    IN actuali_Id_pedido INT,
    IN actuali_valor_pedido BIGINT,
    IN actuali_direccion_pedido VARCHAR(40),
    IN actuali_fecha_soli_pedido DATE,
    IN actuali_Estado_pedido VARCHAR(30),
    IN actuali_Id_cliente_fk_pedido BIGINT
)
BEGIN
    UPDATE Pedido
    SET valor_pedido = actuali_valor_pedido,
        direccion_pedido = actuali_direccion_pedido,
        fecha_soli_pedido = actuali_fecha_soli_pedido,
        Estado_pedido = actuali_Estado_pedido,
        Id_cliente_fk_pedido = actuali_Id_cliente_fk_pedido
    WHERE Id_pedido = actuali_Id_pedido;
END$$

DELIMITER $$

CREATE PROCEDURE actualizar_Produccion (
    IN actuali_Id_produccion INT,
    IN actuali_Fecha_ini_producc DATE,
    IN actuali_Fecha_fin_producc DATE,
    IN actuali_cantidad_producida INT,
    IN actuali_Estado_produccion VARCHAR(30),
    IN actuali_Costo_total BIGINT,
    IN actuali_Id_producto_fk_produccion INT
)
BEGIN
    UPDATE Produccion
    SET Fecha_ini_producc = actuali_Fecha_ini_producc,
        Fecha_fin_producc = actuali_Fecha_fin_producc,
        cantidad_producida = actuali_cantidad_producida,
        Estado_produccion = actuali_Estado_produccion,
        Costo_total = actuali_Costo_total,
        Id_producto_fk_produccion = actuali_Id_producto_fk_produccion
    WHERE Id_produccion = actuali_Id_produccion;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_Metododepago (
    IN actuali_cod_metododepago INT,
    IN actuali_medio_metododepago VARCHAR(20),
    IN actuali_id_cliente_fk_metododepago BIGINT,
    IN actuali_estado_metodopago BOOLEAN
)
BEGIN
    UPDATE Metododepago
    SET medio_metododepago = actuali_medio_metododepago,
        id_cliente_fk_metododepago = actuali_id_cliente_fk_metododepago,
        estado_metodopago = actuali_estado_metodopago
    WHERE cod_metododepago = actuali_cod_metododepago;
END$$

DELIMITER $$
CREATE PROCEDURE actualizar_descrip_detalle (
    IN actuali_id_descrip INT,
    IN actuali_Id_pedido_fk_descrip_detalle INT,
    IN actuali_Cod_produc_fk_descrip_detalle INT,
    IN actuali_cantidad BIGINT,
    IN actuali_Precio_unitario INT,
    IN actuali_sub_total BIGINT
)
BEGIN
    UPDATE descrip_detalle
    SET Id_pedido_fk_descrip_detalle = actuali_Id_pedido_fk_descrip_detalle,
        Cod_produc_fk_descrip_detalle = actuali_Cod_produc_fk_descrip_detalle,
        cantidad = actuali_cantidad,
        Precio_unitario = actuali_Precio_unitario,
        sub_total = actuali_sub_total
    WHERE id_descrip = actuali_id_descrip;
END$$


