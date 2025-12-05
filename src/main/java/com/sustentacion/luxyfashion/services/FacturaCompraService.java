package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.FacturaCompra;

import java.util.List;

public interface FacturaCompraService {
    FacturaCompra guardar(FacturaCompra facturacompra);

    void eliminar(Integer id);

    List<FacturaCompra> listar();

    List<FacturaCompra> findAllByOrderAsc();

    List<FacturaCompra> buscarvarioscampos(String filtro);
}
