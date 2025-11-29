package com.sustentacion.luxyfashion.repositories;


import org.springframework.data.jpa.repository.JpaRepository;
import com.sustentacion.luxyfashion.models.Rol;

//Es el que ejecuta, ejemplo el que guarda en la BD

//JPARepository ya tiene la crud incluida, findAll-> listar, save->guardar, deleteById-> eliminar, findById-> buscar por id
public interface RolRepositories extends JpaRepository<Rol, Integer> {
}

