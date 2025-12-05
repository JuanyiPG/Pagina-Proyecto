package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.DetFactCompra;
import com.sustentacion.luxyfashion.repositories.DetFactCompraRepositories;
import com.sustentacion.luxyfashion.services.DetFactCompraService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class DetFactCompraServiceslmpl implements DetFactCompraRepositories{

    private final DetFactCompraRepositories detFactCompraRepositories;

    public DetFactCompraServiceslmpl(DetFactCompraRepositories detFactCompraRepositories) {
        this.detFactCompraRepositories = detFactCompraRepositories;
    }

    @Override
    public DetFactCompra guardar(DetFactCompra det) {
        return detFactCompraRepositories.save(det);
    }

    @Override
    public void eliminar(Integer id) {
        detFactCompraRepositories.deleteById(id);
    }

    @Override
    public List<DetFactCompra> listar() {
        return detFactCompraRepositories.findAll();
    }

    @Override
    public List<DetFactCompra> findAllByOrderAsc() {
        return detFactCompraRepositories.findAllByOrderByCantAsc();
    }

    @Override
    public List<DetFactCompra> buscarvarioscampos(String filtro) {
        return detFactCompraRepositories.buscarvarioscampos(filtro);
    }
}
