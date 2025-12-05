package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Produccion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ProduccionRepositories extends JpaRepository<Produccion, Integer> {
    List<Produccion> findAllByOrderByFechaIniProduccAsc();

    @Query("SELECT prc FROM Produccion prc WHERE " +
    "CAST(prc.id_producc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.fechaIniProducc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.cant_producc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.costo_mano_obra_producc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.costo_mat_producc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.costo_iva_producc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.costo_total_producc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
    "CAST(prc.fecha_fin_producc AS string) LIKE CONCAT('%', :filtro, '%')"
    )

    List<Produccion> buscarvarioscampos (@Param("filtro")String filtro);
}
