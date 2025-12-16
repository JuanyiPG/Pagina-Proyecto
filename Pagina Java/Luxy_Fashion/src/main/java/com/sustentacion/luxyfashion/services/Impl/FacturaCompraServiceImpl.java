package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.FacturaCompra;
import com.sustentacion.luxyfashion.repositories.FacturaCompraRepositories;
import com.sustentacion.luxyfashion.services.FacturaCompraService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class FacturaCompraServiceImpl implements FacturaCompraService{
    private final FacturaCompraRepositories facturacomprarepositories;

    public FacturaCompraServiceImpl(FacturaCompraRepositories facturacomprarepositories) {
        this.facturacomprarepositories = facturacomprarepositories;
    }

    @Override
    public FacturaCompra guardar(FacturaCompra facturacompra){
        return facturacomprarepositories.save(facturacompra);
    }


    @Override
    public void eliminar(Integer id){
        facturacomprarepositories.deleteById(id);
    }


    @Override
    public List<FacturaCompra> listar(){
        return facturacomprarepositories.findAll();
    }


    @Override
    public List<FacturaCompra> findAllByOrderAsc(){
        return facturacomprarepositories.findAllByOrderByFechafactucAsc();
    }


    @Override
    public List<FacturaCompra> buscarvarioscampos(String filtro){
        return facturacomprarepositories.buscarvarioscampos(filtro);
    }
    @Override
    public FacturaCompra buscarPorId(Integer id){
        return facturacomprarepositories.findById(id).orElse(null);
    }
}
