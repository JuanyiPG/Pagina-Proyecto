package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.FacturaVenta;
import org.springframework.stereotype.Service;

import java.util.List;

public interface FacturaVentaService {
    FacturaVenta guardar(FacturaVenta facturaventa);

    void eliminar(Integer id);

    List<FacturaVenta> listar();

    List<FacturaVenta> findAllByOrderAsc();

    List<FacturaVenta> buscarvarioscampos(String filtro);

    FacturaVenta buscarPorId (Integer id);
}
