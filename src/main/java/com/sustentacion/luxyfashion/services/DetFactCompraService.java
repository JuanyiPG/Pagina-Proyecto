package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.DetFactCompra;
import org.springframework.stereotype.Service;

import java.util.List;

public interface DetFactCompraService {
    DetFactCompra guardar(DetFactCompra det);

    void eliminar(Integer id);

    List<DetFactCompra> listar();

    List<DetFactCompra> findAllByOrderAsc();

    List<DetFactCompra> buscarvarioscampos(String filtro);
}
