package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface AbonoRepositories extends JpaRepository <AbonoRepositories, Integer> {
    List<Empleado> findAllByOrderByFechaAbonoAsc();

    @Query("SELECT Ab FROM Abono Ab WHERE" +
    "CAST(id_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fechaabono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(monto_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(metodo_pago) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(descripcion) LIKE LOWER(CONCAT('%', :filtro, '%'))"
    )

    List<Abono> buscarvarioscampos(@Param("filtro")String filtro);
}

