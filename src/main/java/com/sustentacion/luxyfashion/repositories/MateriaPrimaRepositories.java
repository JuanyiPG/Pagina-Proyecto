package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.MateriaPrima;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MateriaPrimaRepositories extends JpaRepository<MateriaPrima, Integer> {
    List<MateriaPrima> findAllByOrderByNomMatpAsc();

    @Query ("SELECT mp FROM MateriaPrima mp WHERE " +
            "CAST(mp.id_matp AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(CAST(mp.nomMatp AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR "+
            "LOWER(CAST(mp.color AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR "+
            "LOWER(CAST(mp.categoria AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR "+
            "LOWER(CAST(mp.tipo AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR "+
            "CAST(mp.stock_act AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(mp.stock_min AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(CAST(mp.desc_matp AS string)) LIKE LOWER(CONCAT('%', :filtro, '%'))"
    )

    List<MateriaPrima> buscarvarioscampos(@Param("filtro")String filtro);


}
