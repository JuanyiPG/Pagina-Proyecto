package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Producto;

import java.util.List;

public interface ProductoService {

    Producto guardar(Producto producto);

    void eliminar(Integer id);

    List<Producto> listar();

    List<Producto> listaproductoasc();

    List<Producto> buscarvarioscampos(String filtro);

    List<Producto>  findAllByorderAsc();
}
