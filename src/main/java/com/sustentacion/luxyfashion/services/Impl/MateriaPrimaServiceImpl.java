package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.MateriaPrima;
import com.sustentacion.luxyfashion.repositories.MateriaPrimaRepositories;
import com.sustentacion.luxyfashion.services.MateriaPrimaService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class MateriaPrimaServiceImpl implements MateriaPrimaService {
    private final MateriaPrimaRepositories materiaPrimaRepositorio;

    public MateriaPrimaServiceImpl(MateriaPrimaRepositories materiaPrimaRepositorio) {
        this.materiaPrimaRepositorio = materiaPrimaRepositorio;
    }


    @Override
    public MateriaPrima guardar(MateriaPrima materiaprima){
        return materiaPrimaRepositorio.save(materiaprima);
    }


    @Override
    public void eliminar(Integer id){
        materiaPrimaRepositorio.deleteById(id);
    }


    @Override
    public List<MateriaPrima> findAllByOrderAsc(){
        return  materiaPrimaRepositorio.findAllByOrderByNomMatpAsc();
    }


    @Override
    public List<MateriaPrima> buscarvarioscampos(String filtro){
        return materiaPrimaRepositorio.buscarvarioscampos(filtro);
    }



    @Override
    public List<MateriaPrima> listar(){
        return materiaPrimaRepositorio.findAll();
    }

}
