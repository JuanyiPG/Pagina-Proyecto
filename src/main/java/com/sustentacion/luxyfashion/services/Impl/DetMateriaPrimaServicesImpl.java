package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import com.sustentacion.luxyfashion.repositories.DetMateriaPrimaRepositories;
import com.sustentacion.luxyfashion.services.DetMateriaPrimaService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class DetMateriaPrimaServicesImpl implements DetMateriaPrimaService {
private final DetMateriaPrimaRepositories detmateriaprimarepositories;

    public DetMateriaPrimaServicesImpl(DetMateriaPrimaRepositories detmateriaprimarepositories) {
        this.detmateriaprimarepositories = detmateriaprimarepositories;
    }

    @Override
    public DetMateriaPrima guardar(DetMateriaPrima detmateriaprima){
        return  detmateriaprimarepositories.save(detmateriaprima);
    }


    @Override
    public void eliminar(Integer id){
        detmateriaprimarepositories.deleteById(id);
    }


    @Override
    public List<DetMateriaPrima> listar(){
        return  detmateriaprimarepositories.findAll();
    }


    @Override
    public List<DetMateriaPrima> finAllByOrderAsc(){
        return detmateriaprimarepositories.findAllByOrderByDescDetAsc();
    }


    @Override
    public List<DetMateriaPrima> buscarvarioscampos(String filtro){
        return detmateriaprimarepositories.buscarvarioscampos(filtro);
    }
}
