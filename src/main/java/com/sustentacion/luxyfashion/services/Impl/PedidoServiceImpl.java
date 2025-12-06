package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Pedido;
import com.sustentacion.luxyfashion.repositories.PedidoRepositorio;
import com.sustentacion.luxyfashion.services.PedidoService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class PedidoServiceImpl implements PedidoService {
    private final PedidoRepositorio pedidoRepositorio;

    public PedidoServiceImpl(PedidoRepositorio pedidoRepositorio){
        this.pedidoRepositorio = pedidoRepositorio;
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
    public List<Pedido> listar(){
        return pedidoRepositorio.findAll();
    }

    @Override
    public List<Pedido> buscarvarioscampos(String filtro) {
        return pedidoRepositorio.buscarvarioscampos(filtro);
    }

    @Override
    public List<Pedido> findAllByOrderAsc() {
        return pedidoRepositorio.findAllByOrderByNomPedAsc();
    }
    @Override
    public Pedido buscarPorId(Integer id){
        return pedidoRepositorio.findById(id).orElse(null);
    }

    @Override
    public List<Pedido> findAllByOrderByNomPedAsc() {
        return List.of();
    }
}
