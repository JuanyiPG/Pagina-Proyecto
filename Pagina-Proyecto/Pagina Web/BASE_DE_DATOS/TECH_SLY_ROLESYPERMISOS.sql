
CREATE USER 'alejandra'@'localhost' IDENTIFIED BY '2987217';
CREATE USER 'juan'@'localhost' IDENTIFIED BY 'juanpw1245';
CREATE USER 'abbigail'@'localhost' IDENTIFIED BY 'bibi44';


GRANT ALL PRIVILEGES ON TECH_SLY.* TO 'alejandra'@'localhost';


GRANT SELECT, INSERT, UPDATE ON TECH_SLY.Producto TO 'juan'@'localhost';
GRANT SELECT, INSERT, UPDATE ON TECH_SLY.Facturacion TO 'juan'@'localhost';
GRANT SELECT ON TECH_SLY.Cliente TO 'juan'@'localhost';


GRANT SELECT ON TECH_SLY.Producto TO 'abbigail'@'localhost';
GRANT SELECT, INSERT ON TECH_SLY.Pedido TO 'abbigail'@'localhost';

FLUSH PRIVILEGES;

