package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Producto;
import com.sustentacion.luxyfashion.repositories.ProductoRepositories;
import com.sustentacion.luxyfashion.services.ProductoService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class ProductoServiceImpl implements ProductoService {
    private final ProductoRepositories productorepositorio;

    public ProductoServiceImpl(ProductoRepositories productorepositorio) {
        this.productorepositorio = productorepositorio;
    }

    @Override
    public Producto guardar(Producto producto){
        return productorepositorio.save(producto);
    }

    @Override
    public void eliminar(Integer id){
        productorepositorio.deleteById(id);
    }

    @Override
    public List<Producto> listar(){
        return productorepositorio.findAll();
    }

    @Override
    public List<Producto> listaproductoasc(){
        return  productorepositorio.findByOrderByNomProducAsc();
    }

    @Override
    public List<Producto> buscarvarioscampos(String filtro){
        return productorepositorio.buscarvarioscampos(filtro);
    }

    @Override
    public List<Producto>  findAllByorderAsc(){
        return productorepositorio.findByOrderByNomProducAsc();
    }
}
