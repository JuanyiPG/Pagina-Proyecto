package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AbonoRepositories extends JpaRepository <AbonoRepositories, Integer> {
    List<Empleado> findAllByOrderByNomEmpleAsc();
}

