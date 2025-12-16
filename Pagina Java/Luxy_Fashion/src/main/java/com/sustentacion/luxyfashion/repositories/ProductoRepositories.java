package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ProductoRepositories extends JpaRepository<Producto, Integer> {
    List<Producto> findByOrderByNomProducAsc();

    @Query("SELECT prd FROM Producto prd WHERE " +
            "CAST(prd.id_produc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(prd.link_produc) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(prd.nomProduc) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(prd.desc_produc) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(prd.categoria_produc) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(prd.unid_med_produc) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Producto> buscarvarioscampos(@Param("filtro") String filtro);

}
