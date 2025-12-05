package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.DetFactProducto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface DetFactProductoRepositories extends JpaRepository<DetFactProducto, Integer> {

    // Traer todos los registros ordenados por descripción
    List<DetFactProducto> findAllByOrderByDescrDetAsc();
<<<<<<< HEAD

=======
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf

    // Búsqueda por varios campos
    @Query("SELECT d FROM DetFactProducto d WHERE " +
            "CAST(d.id_det AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(d.descrDet) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "CAST(d.facturaVenta.id_factuv AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(d.producto.id_produc AS string) LIKE CONCAT('%', :filtro, '%')")
    List<DetFactProducto> buscarvarioscampos(@Param("filtro") String filtro);

}
