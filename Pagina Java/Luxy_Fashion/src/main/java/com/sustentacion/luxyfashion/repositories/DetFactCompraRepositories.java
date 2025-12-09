package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.DetFactCompra;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface DetFactCompraRepositories extends JpaRepository<DetFactCompra, Integer> {

    // Traer todos los registros ordenados por cantidad
    List<DetFactCompra> findAllByOrderByCantAsc();

    // Búsqueda por varios campos
    @Query("SELECT d FROM DetFactCompra d WHERE " +
            "CAST(d.id_det_fcm AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(d.cant AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(d.desc_det) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "CAST(d.facturaCompra.id_factuc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(d.materiaPrima.id_matp AS string) LIKE CONCAT('%', :filtro, '%')")
    List<DetFactCompra> buscarvarioscampos(@Param("filtro") String filtro);

}
