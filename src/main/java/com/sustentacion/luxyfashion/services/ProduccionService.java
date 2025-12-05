package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Produccion;

import java.util.List;

public interface ProduccionService {
    Produccion guardar(Produccion produccion);

    void eliminar(Integer id);

    List<Produccion> listar();

    List<Produccion> buscarvarioscampos(String filtro);

    List<Produccion> findAllByOrderAsc();
}
