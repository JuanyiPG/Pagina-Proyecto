package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface UsuarioRepositories extends JpaRepository<Usuario, Integer> {
    Optional<Usuario> findByUsername(String username);
    boolean existsByUsername(String username);

    @Query("SELECT u FROM Usuario u WHERE " +
            "LOWER(u.username) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(u.contrasena) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Usuario> buscarVariosCampos(@Param("filtro") String filtro);

    List<Usuario> findAllByOrderByUsername();
}

