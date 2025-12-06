package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.DetFactProducto;
import org.springframework.stereotype.Service;

import java.util.List;

public interface DetFactProductoService {
    DetFactProducto guardar(DetFactProducto det);

    void eliminar(Integer id);

    List<DetFactProducto> listar();

    List<DetFactProducto> findAllByOrderAsc();

    List<DetFactProducto> buscarvarioscampos(String filtro);
}
