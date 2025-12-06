package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface UsuarioRepositories extends JpaRepository<Usuario, Integer> {
    List<Usuario> findAllByOrderByUsername();
    @Query("SELECT r FROM Usuario r WHERE " +
            "LOWER(r.username) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(r.contraseña) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Usuario> buscarVariosCampos(@Param("filtro") String filtro);


    boolean existsByUsername (String username);
    // Para el login
    Usuario findByUsernameAndContraseña(String username, String contraseña);}
