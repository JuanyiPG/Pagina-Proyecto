package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.FacturaCompra;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface FacturaCompraRepositories extends JpaRepository<FacturaCompra, Integer> {
    List<FacturaCompra> findAllByOrderByFechafactucAsc();

    @Query("SELECT fc FROM FacturaCompra fc WHERE " +
    "CAST(fc.id_factuc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fc.fechafactuc AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fc.total AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(fc.metodo_pago) LIKE LOWER(CONCAT('%', :filtro, '%'))"
    )

    List<FacturaCompra> buscarvarioscampos(@Param("filtro")String filtro);

}
