package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ClienteRepositories extends JpaRepository<Cliente, Integer> {
    List<Cliente> findAllByOrderByNomClienAsc();
    @Query("SELECT r FROM Cliente r WHERE " +
            "LOWER(r.nomClien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.dir_clien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.tel_clien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.correo) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.usuario_clien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.contra_clien) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Cliente> buscarVariosCampos(@Param("filtro") String filtro);

    boolean existsByCorreo(String correo); //Consulta para comprobar que el correo no este duplicado o ya existe.
}
