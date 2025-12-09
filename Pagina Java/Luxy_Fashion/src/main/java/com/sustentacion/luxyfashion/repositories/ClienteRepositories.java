package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface ClienteRepositories extends JpaRepository<Cliente, Integer> {
    Optional<Cliente> findByUsuario(String usuario);
    boolean existsByCorreo(String correo);
    boolean existsByUsuario(String usuario);
    List<Cliente> findAllByOrderByNomClienAsc();

    @Query("SELECT r FROM Cliente r WHERE " +
            "LOWER(r.nomClien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.dir_clien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.tel_clien) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.correo) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.usuario) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.contra_clien) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Cliente> buscarVariosCampos(@Param("filtro") String filtro);
}

