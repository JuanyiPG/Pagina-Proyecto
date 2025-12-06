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
    private final MateriaPrimaRepositories materiaPrimaRepositorio;
    private final DetMateriaPrimaRepositories detMateriaPrimaRepositorio;

<<<<<<< HEAD:src/main/java/com/sustentacion/luxyfashion/services/Impl/MateriaPrimaServicelmpl.java
    public MateriaPrimaServicelmpl(MateriaPrimaRepositories materiaPrimaRepositorio,  DetMateriaPrimaRepositories detMateriaPrimaRepositorio) {
=======
    public MateriaPrimaServiceImpl(MateriaPrimaRepositories materiaPrimaRepositorio) {
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf:src/main/java/com/sustentacion/luxyfashion/services/Impl/MateriaPrimaServiceImpl.java
        this.materiaPrimaRepositorio = materiaPrimaRepositorio;
        this.detMateriaPrimaRepositorio = detMateriaPrimaRepositorio;
    }


    @Override
    public MateriaPrima guardar(MateriaPrima materiaprima){
        return materiaPrimaRepositorio.save(materiaprima);
    }

    @Override
    public DetMateriaPrima guardar(DetMateriaPrima detmateriaprima) {
        return detMateriaPrimaRepositorio.save(detmateriaprima);
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
    public List<DetMateriaPrima> finAllByOrderAsc() {
        return List.of();
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
