package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Abono;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface AbonoRepositories extends JpaRepository<Abono, Integer> {
    List<Abono> findAllByOrderByFechaAbonoAsc();

    @Query("SELECT Ab FROM Abono Ab WHERE " +
    "CAST(Ab.id_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(Ab.fechaAbono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(Ab.monto_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(Ab.metodo_pago) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(Ab.descripcion) LIKE LOWER(CONCAT('%', :filtro, '%'))"
    )

    List<Abono> buscarvarioscampos(@Param("filtro")String filtro);
}

