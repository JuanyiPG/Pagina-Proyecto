package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Producto;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductoRepositories extends JpaRepository<Producto, Integer> {
}
