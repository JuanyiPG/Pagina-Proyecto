package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Pedido;
import com.sustentacion.luxyfashion.repositories.PedidoRepositorio;
import com.sustentacion.luxyfashion.services.PedidoService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PedidoServicelmpl implements PedidoService {
    private final PedidoRepositorio pedidoRepositorio;

    public PedidoServicelmpl(PedidoRepositorio pedidoRepositorio){
        this.pedidoRepositorio = pedidoRepositorio;
    }

    @Override
    public List<Pedido> listar(){
        return pedidoRepositorio.findAll();
    }
    @Override
    public List<Pedido> listapedidoasc(){
        return pedidoRepositorio.findAllByOrderByNomPedAsc();
    }
    @Override
    public Pedido guardar(Pedido pedido){
        return pedidoRepositorio.save(pedido);
    }
    @Override
    public void eliminar(Integer id){
        pedidoRepositorio.deleteById(id);
    }

    @Override
    public List<Pedido> buscarVariosCampos(String filtro) {
        return pedidoRepositorio.buscarvarioscampos(filtro);
    }

    @Override
    public List<Pedido> findAllByOrderByNomPedAsc() {
        return pedidoRepositorio.findAllByOrderByNomPedAsc();
    }
}
