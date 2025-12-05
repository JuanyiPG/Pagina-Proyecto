package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.DetFactProducto;
import com.sustentacion.luxyfashion.repositories.DetFactProductoRepositories;
import com.sustentacion.luxyfashion.services.DetFactProductoService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class DetFactProductoServiceslmpl implements DetFactProductoService {

    private final DetFactProductoRepositories detFactProductoRepositories;

    public DetFactProductoServiceslmpl(DetFactProductoRepositories detFactProductoRepositories) {
        this.detFactProductoRepositories = detFactProductoRepositories;
    }

    @Override
    public DetFactProducto guardar(DetFactProducto det) {
        return detFactProductoRepositories.save(det);
    }

    @Override
    public void eliminar(Integer id) {
        detFactProductoRepositories.deleteById(id);
    }

    @Override
    public List<DetFactProducto> listar() {
        return detFactProductoRepositories.findAll();
    }

    @Override
    public List<DetFactProducto> findAllByOrderAsc() {
        return detFactProductoRepositories.findAllByOrderByDescrDetAsc();
    }

    @Override
    public List<DetFactProducto> buscarvarioscampos(String filtro) {
        return detFactProductoRepositories.buscarvarioscampos(filtro);
    }
}
