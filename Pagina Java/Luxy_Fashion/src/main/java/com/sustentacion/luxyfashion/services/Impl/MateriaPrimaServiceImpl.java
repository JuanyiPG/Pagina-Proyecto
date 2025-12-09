package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import com.sustentacion.luxyfashion.models.MateriaPrima;
import com.sustentacion.luxyfashion.repositories.DetMateriaPrimaRepositories;
import com.sustentacion.luxyfashion.repositories.MateriaPrimaRepositories;
import com.sustentacion.luxyfashion.services.MateriaPrimaService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class MateriaPrimaServiceImpl implements MateriaPrimaService {
    private final MateriaPrimaRepositories materiaPrimaRepositories;
    private final DetMateriaPrimaRepositories detMateriaPrimaRepositories;


    public MateriaPrimaServiceImpl(MateriaPrimaRepositories materiaPrimaRepositories, DetMateriaPrimaRepositories detMateriaPrimaRepositories) {

        this.materiaPrimaRepositories = materiaPrimaRepositories;
        this.detMateriaPrimaRepositories = detMateriaPrimaRepositories;
    }


    @Override
    public MateriaPrima guardar(MateriaPrima materiaprima){
        return materiaPrimaRepositories.save(materiaprima);
    }


    @Override
    public void eliminar(Integer id){
        materiaPrimaRepositories.deleteById(id);
    }


    @Override
    public List<MateriaPrima> findAllByOrderAsc(){
        return  materiaPrimaRepositories.findAllByOrderByNomMatpAsc();
    }



    @Override
    public List<MateriaPrima> buscarvarioscampos(String filtro){
        return materiaPrimaRepositories.buscarvarioscampos(filtro);
    }



    @Override
    public List<MateriaPrima> listar(){
        return materiaPrimaRepositories.findAll();
    }

}
