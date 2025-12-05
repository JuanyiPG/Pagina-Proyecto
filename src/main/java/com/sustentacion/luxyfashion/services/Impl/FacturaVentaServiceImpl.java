package com.sustentacion.luxyfashion.services.Impl;


import com.sustentacion.luxyfashion.models.FacturaVenta;
import com.sustentacion.luxyfashion.repositories.FacturaVentaRepositories;
import com.sustentacion.luxyfashion.services.FacturaVentaService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class FacturaVentaServiceImpl implements FacturaVentaService {
    private final FacturaVentaRepositories facturaventarepositories;

    public FacturaVentaServiceImpl(FacturaVentaRepositories facturaventarepositories) {
        this.facturaventarepositories = facturaventarepositories;
    }

    @Override
    public FacturaVenta guardar(FacturaVenta facturaventa){
        return facturaventarepositories.save(facturaventa);
    }


    @Override
    public void eliminar(Integer id){
        facturaventarepositories.deleteById(id);
    }


    @Override
    public List<FacturaVenta> listar(){
        return facturaventarepositories.findAll();
    }


    @Override
    public List<FacturaVenta> findAllByOrderAsc(){
        return  facturaventarepositories.findAllByOrderByFechafactuvAsc();
    }


    @Override
    public List<FacturaVenta> buscarvarioscampos(String filtro){
        return  facturaventarepositories.buscarvarioscampos(filtro);
    }

    @Override
    public FacturaVenta buscarPorId(Integer id){
        return facturaventarepositories.findById(id).orElse(null);
    }
}
