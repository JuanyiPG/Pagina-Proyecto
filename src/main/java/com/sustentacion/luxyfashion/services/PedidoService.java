package com.sustentacion.luxyfashion.services;

import org.springframework.stereotype.Service;
import com.sustentacion.luxyfashion.models.Pedido;
import org.springframework.stereotype.Service;

import java.util.List;


public interface PedidoService {

    List<Pedido> listar();

    Pedido guardar(Pedido pedido);

    void eliminar(Integer id);

    List<Pedido> buscarvarioscampos(String filtro);

    Pedido buscarPorId(Integer id);

    List<Pedido> findAllByOrderByNomPedAsc();

    List<Pedido> findAllByOrderAsc();
}
