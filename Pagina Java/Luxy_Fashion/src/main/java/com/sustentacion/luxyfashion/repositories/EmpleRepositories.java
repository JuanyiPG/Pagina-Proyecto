package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface EmpleRepositories extends JpaRepository<Empleado, Integer> {
    List<Empleado> findAllByOrderByNomEmpleAsc();

    @Query("SELECT r FROM Empleado r WHERE " +
            "r.nomEmple LIKE CONCAT('%', :filtro, '%') OR " +
            "r.tel_emple LIKE CONCAT('%', :filtro, '%') OR " +
            "r.correo LIKE CONCAT('%', :filtro, '%') OR " +
            "r.tipo_ident LIKE CONCAT('%', :filtro, '%') OR " +
            "r.num_ident LIKE CONCAT('%', :filtro, '%') OR " +
            "r.estado_emple LIKE CONCAT('%', :filtro, '%')")
    List<Empleado> buscarVariosCampos(@Param("filtro") String filtro);

    boolean existsByCorreo(String correo);
    boolean existsByCorreoAndIdEmpleNot(String correo, Integer idEmple);


}
