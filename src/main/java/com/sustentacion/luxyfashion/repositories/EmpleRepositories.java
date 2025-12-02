package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface EmpleRepositories extends JpaRepository<Empleado, Integer> {
    List<Empleado> findAllByOrderByNomEmpleAsc();

    //El query se usa para hacer consultas personalizadas JPA o MYSQL
    @Query("SELECT r FROM Empleado r WHERE " +   //Nombre de la entidad
            "r.tel_emple LIKE CONCAT('%', :filtro, '%') OR " +// el atributo, por ello se coloca r
            "r.correo_emple LIKE CONCAT('%', :filtro, '%') OR " +
            "r.tipo_identificacion LIKE CONCAT('%', :filtro, '%') OR " +
            "r.num_indetificacion LIKE CONCAT('%', :filtro, '%') OR " +
            "r.estado_emple LIKE CONCAT('%', :filtro, '%') OR " +
            "r.usuario LIKE CONCAT('%', :filtro, '%')")
    List<Empleado> buscarVariosCampos(@Param("filtro") String filtro);


}
