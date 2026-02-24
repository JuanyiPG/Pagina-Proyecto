package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Produccion;
import com.sustentacion.luxyfashion.repositories.ProduccionRepositories;
import com.sustentacion.luxyfashion.services.ProduccionService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class ProduccionServiceImpl implements ProduccionService {
    private final ProduccionRepositories produccionrepositorio;

    public ProduccionServiceImpl(ProduccionRepositories produccionrepositorio) {
        this.produccionrepositorio = produccionrepositorio;
    }

    @Override
    public Produccion guardar(Produccion produccion){
        return produccionrepositorio.save(produccion);
    }

    @Transactional
    public void eliminar(Integer id){
        produccionrepositorio.deleteById(id);
        produccionrepositorio.flush();
    }

    @Override
    public List<Produccion> listar(){
        return produccionrepositorio.findAll();
    }

    @Override
    public List<Produccion> buscarvarioscampos(String filtro){
        return produccionrepositorio.buscarvarioscampos(filtro);
    }

    @Override
    public List<Produccion> findAllByOrderAsc(){
        return produccionrepositorio.findAllByOrderByFechaIniProduccAsc();
    }

    @Override
    public Produccion buscarPorId(Integer id){
        return produccionrepositorio.findById(id).orElse(null);
    }
}
