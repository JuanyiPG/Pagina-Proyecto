package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Pedido;
import org.springframework.stereotype.Service;

import java.util.List;
public interface PedidoService {

    List<Pedido> listar();

    List<Pedido> listapedidoasc();

    Pedido guardar(Pedido pedido);

    void eliminar(Integer id);

    List<Pedido> buscarVariosCampos(String filtro);

    List<Pedido> findAllByOrderAsc();
}
