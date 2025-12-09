package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.FacturaVenta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface FacturaVentaRepositories extends JpaRepository<FacturaVenta, Integer> {
    List<FacturaVenta> findAllByOrderByFechafactuvAsc();

    @Query("SELECT fv FROM FacturaVenta fv WHERE " +
    "CAST(fv.id_factuv AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fv.fechafactuv AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fv.subtotal_factuv AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fv.iva_factuv AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fv.total_factuv AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fv.metodo_pago AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fv.descu_factuv AS string) LIKE CONCAT('%', :filtro, '%') "
    )

    List<FacturaVenta> buscarvarioscampos(@Param("filtro")String filtro);
}
