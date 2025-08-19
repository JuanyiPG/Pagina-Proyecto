use TECH_SLY

DELIMITER $$

CREATE PROCEDURE insrt_Empleado(
  IN insrt_Id_emple BIGINT,
  IN insrt_Nom_empleado VARCHAR(30),
  IN insrt_fech_ingre_emple DATE,
  IN insrt_RH_emple VARCHAR(5),
  IN insrt_salario_emple NUMERIC,
  IN insrt_fech_naci_emple DATE,
  IN insrt_direc_emple VARCHAR(30),
  IN insrt_estado_emple BOOLEAN
)
BEGIN
  INSERT INTO Empleado (Id_emple, Nom_empleado, fech_ingre_emple, RH_emple,
  salario_emple, fech_naci_emple, direc_emple, estado_emple) 
  VALUES (
    insrt_Id_emple, insrt_Nom_empleado, insrt_fech_ingre_emple, insrt_RH_emple,
    insrt_salario_emple, insrt_fech_naci_emple, insrt_direc_emple ,insrt_estado_emple
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Telef_empleado(
  IN insrt_Id_telef_emple INT,
  IN insrt_telef_emple_1 NUMERIC,
  IN insrt_Id_emple_fk_telef_emple BIGINT
)
BEGIN
  INSERT INTO Telef_empleado (Id_telef_emple, telef_emple_1, Id_emple_fk_telef_emple)
  VALUES (
    insrt_Id_telef_emple, insrt_telef_emple_1, insrt_Id_emple_fk_telef_emple
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Correo_emple(
  IN insrt_Id_correo_emple INT,
  IN insrt_correo_emple_1 VARCHAR(40),
  IN insrt_Id_emple_fk_correo_emple BIGINT
)
BEGIN
  INSERT INTO Correo_emple (Id_correo_emple, correo_emple_1, Id_emple_fk_correo_emple) 
  VALUES (
    insrt_Id_correo_emple, insrt_correo_emple_1, insrt_Id_emple_fk_correo_emple
  );
END$$

DELIMITER $$
  CREATE PROCEDURE insrt_Cliente(
  IN insrt_Id_cliente BIGINT,
  IN insrt_Nom_cliente VARCHAR (30),
  IN insrt_fecha_naci_clien DATE,
  IN insrt_ciudad_cliente VARCHAR (30),
  in insrt_estado_cliente BOOLEAN
)
BEGIN
  INSERT INTO Cliente (Id_cliente, Nom_cliente, fecha_naci_clien, ciudad_cliente, estado_cliente)
  VALUES (insrt_Id_cliente, insrt_Nom_cliente, insrt_fecha_naci_clien, insrt_ciudad_cliente, insrt_estado_cliente);
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Telef_clien(
  IN insrt_Id_telef_cliente INT,
  IN insrt_telf_cliente_1 NUMERIC,
  IN insrt_Id_cliente_fk_telef_cliente BIGINT
)
BEGIN
  INSERT INTO Telef_clien (Id_telef_cliente, telf_cliente_1, Id_cliente_fk_telef_cliente)
  VALUES (insrt_Id_telef_cliente, insrt_telf_cliente_1, insrt_Id_cliente_fk_telef_cliente);
END$$

DELIMITER $$
  CREATE PROCEDURE insrt_correo_client(
  IN insrt_Id_correo_client INT,
  IN insrt_correo_client_1 VARCHAR(40),
  IN insrt_Id_cliente_fk_correo_client BIGINT
)
BEGIN
  INSERT INTO correo_client (Id_correo_client, correo_client_1, Id_cliente_fk_correo_client)
  VALUES (
    insrt_Id_correo_client, insrt_correo_client_1, insrt_Id_cliente_fk_correo_client
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Usuarios(
  IN insrt_Id_usuario INT,
  IN insrt_Nom_usuario VARCHAR(30),
  IN insrt_Contraseña VARCHAR(40),
  IN insrt_estado_usuario BOOLEAN
)
BEGIN
  INSERT INTO Usuarios(Id_usuario, Nom_usuario, Contraseña, estado_usuario)
  VALUES (insrt_Id_usuario, insrt_Nom_usuario, insrt_Contraseña, insrt_estado_usuario
  );
END$$
  
  
  DELIMITER $$

CREATE PROCEDURE insrt_Usuari_emple (
    IN insrt_Id_usu_emple INT,
    IN insrt_Id_emple_fk_usuari_emple BIGINT
)
BEGIN
    INSERT INTO Usuari_emple (Id_usu_emple, Id_emple_fk_usuari_emple)
    VALUES (insrt_Id_usu_emple, insrt_Id_emple_fk_usuari_emple);
END$$

DELIMITER $$

CREATE PROCEDURE insrt_Usuari_cliente (
    IN insrt_Id_usu_clen INT,
    IN insrt_Id_clien_fk_usuari_cliente BIGINT
)
BEGIN
    INSERT INTO usuari_cliente (Id_usu_clen, Id_clien_fk_usuari_cliente)
    VALUES (insrt_Id_usu_clen, insrt_Id_clien_fk_usuari_cliente);
END$$


DELIMITER $$
CREATE PROCEDURE insrt_Facturacion(
  IN insrt_Cod_factu INT,
  IN insrt_fecha_factu DATE,
  IN insrt_IVA_factu BIGINT,
  IN insrt_subtotal_factu BIGINT,
  IN insrt_Total_factu BIGINT,
  IN insrt_Id_emple_fk_facturacion BIGINT,
  IN insrt_estado_facturacion BOOLEAN
)
BEGIN
  INSERT INTO Facturacion (Cod_factu, fecha_factu, IVA_factu, subtotal_factu, Total_factu,
  Id_emple_fk_facturacion, estado_facturacion) 
  VALUES (
    insrt_Cod_factu, insrt_fecha_factu, insrt_IVA_factu, insrt_subtotal_factu, 
    insrt_Total_factu, insrt_Id_emple_fk_facturacion, insrt_estado_facturacion
   );
END$$



DELIMITER $$


CREATE PROCEDURE insrt_Producto(
  IN insrt_Cod_produc                 INT,
  IN insrt_Nom_produc                 VARCHAR(30),
  IN insrt_talla_producto             VARCHAR(15),
  IN insrt_color_producto             VARCHAR(10),
  IN insrt_Categoria_producto         VARCHAR(30),
  IN insrt_Materi_produc              VARCHAR(30),
  IN insrt_Medida_produc              NUMERIC,
  IN insrt_Cant_produc                NUMERIC,
  IN insrt_Cant_minima                BIGINT,
  IN insrt_valor_produc               BIGINT,
  IN insrt_estilo_producto            VARCHAR(30),
  IN insrt_descripcion_producto       VARCHAR(50),
  IN insrt_estado_produ               BOOLEAN
)
BEGIN
  INSERT INTO Producto (
    Cod_produc, Nom_produc, talla_producto, color_producto,
    Categoria_producto, Materi_produc, Medida_produc, Cant_produc,
    Cant_minima, valor_produc, estilo_producto, descripcion_producto,
    estado_produ
  )
  VALUES (
    insrt_Cod_produc, insrt_Nom_produc, insrt_talla_producto, insrt_color_producto,
    insrt_Categoria_producto, insrt_Materi_produc, insrt_Medida_produc, insrt_Cant_produc,
    insrt_Cant_minima, insrt_valor_produc, insrt_estilo_producto, insrt_descripcion_producto,
    insrt_estado_produ
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Materia_prima(
  IN insrt_Id_materia                       INT,
  IN insrt_Nom_materia_prima                VARCHAR(40),
  IN insrt_Tipo_material                    VARCHAR(30),
  IN insrt_Color                            VARCHAR(30),
  IN insrt_Stock_actual                     NUMERIC,
  IN insrt_Stock_minimo                     NUMERIC,
  IN insrt_Descripcion                      VARCHAR(50),
  IN insrt_estado_materia                   BOOLEAN,
  IN insrt_Id_producto_fk_materia_prima     INT
)
BEGIN
  INSERT INTO Materia_prima (
    Id_materia, Nom_materia_prima, Tipo_material, Color,
    Stock_actual, Stock_minimo, Descripcion, estado_materia,
    Id_producto_fk_materia_prima
  )
  VALUES (
    insrt_Id_materia, insrt_Nom_materia_prima, insrt_Tipo_material, insrt_Color,
    insrt_Stock_actual, insrt_Stock_minimo, insrt_Descripcion, insrt_estado_materia,
    insrt_Id_producto_fk_materia_prima
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Producto_MateriaPrima(
  IN insrt_id_prod_materia                INT,
  IN insrt_id_producto_fk_prod_materi     INT,
  IN insrt_id_materia_fk_prod_materi      INT,
  IN insrt_cantidad_utilizada             NUMERIC,
  IN insrt_unidad                         VARCHAR(10)
)
BEGIN
  INSERT INTO Producto_MateriaPrima (
    id_prod_materia, id_producto_fk_prod_materi,
    id_materia_fk_prod_materi, cantidad_utilizada, unidad
  )
  VALUES (
    insrt_id_prod_materia, insrt_id_producto_fk_prod_materi,
    insrt_id_materia_fk_prod_materi, insrt_cantidad_utilizada, insrt_unidad
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Compra_materia_prima(
  IN insrt_Id_compra_m                       INT,
  IN insrt_cantidad_compra                   BIGINT,
  IN insrt_valor_compra                      BIGINT,
  IN insrt_descrip_compra                    VARCHAR(50),
  IN insrt_fecha_compra                      DATE,
  IN insrt_Id_Materiaprima_fk_materia_c      INT,
  IN insrt_Estado_compra_m                   BOOLEAN
)
BEGIN
  INSERT INTO Compra_materia_prima (
    Id_compra_m, cantidad_compra, valor_compra,
    descrip_compra, fecha_compra,
    Id_Materiaprima_fk_materia_c, Estado_compra_m
  )
  VALUES (
    insrt_Id_compra_m, insrt_cantidad_compra, insrt_valor_compra,
    insrt_descrip_compra, insrt_fecha_compra,
    insrt_Id_Materiaprima_fk_materia_c, insrt_Estado_compra_m
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Pedido(
  IN insrt_Id_pedido                   INT,
  IN insrt_valor_pedido                BIGINT,
  IN insrt_direccion_pedido            VARCHAR(40),
  IN insrt_fecha_soli_pedido           DATE,
  IN insrt_Estado_pedido               VARCHAR(30),
  IN insrt_Id_cliente_fk_pedido        BIGINT
)
BEGIN
  INSERT INTO Pedido (
    Id_pedido, valor_pedido, direccion_pedido,
    fecha_soli_pedido, Estado_pedido,
    Id_cliente_fk_pedido
  )
  VALUES (
    insrt_Id_pedido, insrt_valor_pedido, insrt_direccion_pedido,
    insrt_fecha_soli_pedido, insrt_Estado_pedido,
    insrt_Id_cliente_fk_pedido
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Produccion(
  IN insrt_Id_produccion                INT,
  IN insrt_Fecha_ini_producc            DATE,
  IN insrt_Fecha_fin_producc            DATE,
  IN insrt_cantidad_producida           INT,
  IN insrt_Estado_produccion            VARCHAR(30),
  IN insrt_Costo_total                  BIGINT,
  IN insrt_Id_producto_fk_produccion    INT
)
BEGIN
  INSERT INTO Produccion (
    Id_produccion, Fecha_ini_producc, Fecha_fin_producc,
    cantidad_producida, Estado_produccion,
    Costo_total, Id_producto_fk_produccion
  )
  VALUES (
    insrt_Id_produccion, insrt_Fecha_ini_producc, insrt_Fecha_fin_producc,
    insrt_cantidad_producida, insrt_Estado_produccion,
    insrt_Costo_total, insrt_Id_producto_fk_produccion
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_Metododepago(
  IN insrt_cod_metododepago             INT,
  IN insrt_medio_metododepago           VARCHAR(20),
  IN insrt_id_cliente_fk_metododepago   BIGINT,
  IN insrt_estado_metodopago            BOOLEAN
)
BEGIN
  INSERT INTO Metododepago (
    cod_metododepago, medio_metododepago,
    id_cliente_fk_metododepago, estado_metodopago
  )
  VALUES (
    insrt_cod_metododepago, insrt_medio_metododepago,
    insrt_id_cliente_fk_metododepago, insrt_estado_metodopago
  );
END$$

DELIMITER $$
CREATE PROCEDURE insrt_descrip_detalle(
  IN insrt_id_descrip                         INT,
  IN insrt_Id_pedido_fk_descrip_detalle       INT,
  IN insrt_Cod_produc_fk_descrip_detalle      INT,
  IN insrt_cantidad                           BIGINT,
  IN insrt_Precio_unitario                    INT,
  IN insrt_sub_total                          BIGINT
)
BEGIN
  INSERT INTO descrip_detalle (
    id_descrip, Id_pedido_fk_descrip_detalle,
    Cod_produc_fk_descrip_detalle, cantidad,
    Precio_unitario, sub_total
  )
  VALUES (
    insrt_id_descrip, insrt_Id_pedido_fk_descrip_detalle,
    insrt_Cod_produc_fk_descrip_detalle, insrt_cantidad,
    insrt_Precio_unitario, insrt_sub_total
  );
END$$


CALL insrt_Administrador(1, 'Laura', '1985-05-10', 2500000, 'Calle 123', 'laura123', 'clave123');
CALL insrt_Telef_adm(1, 3101234567, 3207654321, 1);
CALL insrt_Correo_adm(1, 'laura@mail.com', 'laura2@mail.com', 1);
CALL insrt_Login_adm('laura123', 'clave123', 1);
CALL insrt_Empleado('Carlos', '2022-01-01', 'O+', 1800000, '1990-03-15', 'Cra 45', TRUE, 1);
CALL insrt_Login_Empleado('Carlos', 'claveCarlos', 1);
CALL insrt_Telef_empleado(1, 3001112233, 3002223344, 1);
CALL insrt_Correo_emple(1, 'carlos@mail.com', 'carlos2@mail.com', 1);
CALL insrt_Cliente('Andrea', '1999-07-21', '2024-06-01', 'Bogotá');
CALL insrt_Telef_clien(1, 3124567890, 3139876543, 1);
CALL insrt_correo_client(1, 'andrea@mail.com', 'andrea2@mail.com', 1);
CALL insrt_Login_cliente('andreaUser', 'claveAndrea', 1);
CALL insrt_Facturacion('2024-06-19', 3800, 20000, 23800, 1);
CALL insrt_Producto('Camisa', 'M', 'Azul', 'Camisas', 'Algodón', 1.0, 100, 30000, 'Casual', 'Camisa manga larga azul');
CALL insrt_Entrada(50, '2024-06-15', 'Lote inicial', 1500000, 1);
CALL insrt_Salida(5, '2024-06-18', 'Venta inicial', 150000, 1);
CALL insrt_Pedido(1001, 45000, 'Carrera 10 #20', '2024-06-17', 1);
CALL insrt_Metododepago(1, 'Tarjeta', 1);
CALL insrt_descrip_detalle(1, 1, 1, 3, 15000, 45000);

