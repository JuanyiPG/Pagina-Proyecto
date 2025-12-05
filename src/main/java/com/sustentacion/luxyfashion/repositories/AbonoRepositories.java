package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Abono;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

<<<<<<< HEAD
public interface AbonoRepositories extends JpaRepository <Abono, Integer> {
    List<Abono> findAllByOrderByFechaabonoAsc();

    @Query("SELECT Ab FROM Abono Ab WHERE " +
            "CAST(id_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(fechaabono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(monto_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(metodo_pago) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(descripcion) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Abono> buscarVariosCampos(@Param("filtro") String filtro);
=======
public interface AbonoRepositories extends JpaRepository<Abono, Integer> {
    List<Abono> findAllByOrderByFechaAbonoAsc();

    @Query("SELECT Ab FROM Abono Ab WHERE " +
    "CAST(Ab.id_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(Ab.fechaAbono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "CAST(Ab.monto_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
            "LOWER(Ab.metodo_pago) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(Ab.descripcion) LIKE LOWER(CONCAT('%', :filtro, '%'))"
    )
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf

    interface AbonoRepositories extends JpaRepository <Abono, Integer> {
        List<Abono> findAllByOrderByFechaabonoAsc();

        @Query("SELECT Ab FROM Abono Ab WHERE " +
                "CAST(Ab.id_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
                "CAST(Ab.fechaabono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
                "CAST(Ab.monto_abono AS string) LIKE CONCAT('%', :filtro, '%') OR " +
                "LOWER(Ab.metodo_pago) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
                "LOWER(Ab.descripcion) LIKE LOWER(CONCAT('%', :filtro, '%'))")
        List<Abono> buscarVariosCampos(@Param("filtro") String filtro);
    }
}



