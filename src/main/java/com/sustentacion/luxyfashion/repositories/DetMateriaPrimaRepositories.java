package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface DetMateriaPrimaRepositories extends JpaRepository<DetMateriaPrima, Integer> {

    // Traer todos los registros ordenados por descripción
    List<DetMateriaPrima> findAllByOrderByDescDetAsc();

    // Búsqueda por varios campos
    @Query("SELECT d FROM DetMateriaPrima d WHERE " +
            "CAST(d.id_det_pm AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(d.desc_det) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "CAST(d.materiaPrima.id_matp AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(d.produccion.id_producc AS string) LIKE CONCAT('%', :filtro, '%')")
    List<DetMateriaPrima> buscarvarioscampos(@Param("filtro") String filtro);

}
