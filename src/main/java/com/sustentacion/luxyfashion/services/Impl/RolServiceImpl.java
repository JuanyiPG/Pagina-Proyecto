package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.repositories.RolRepositories;
import com.sustentacion.luxyfashion.services.RolService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;
import com.sustentacion.luxyfashion.models.Rol;

import java.util.List;
@Transactional
@Service
class RolServiceImpl implements RolService {
    private final RolRepositories rolRepositories; //Forma correcta y segura para poder inyectar dependencias.

    //Una inyeccion es darle a la clase un objeto sin que la tenga que crear con new.

    //Inyeccion por Constructor: Se entrega la dependencia al crear el objeto, garantizando que siempre esté lista y no sea null
    public RolServiceImpl(RolRepositories rolRepositories){
        this.rolRepositories = rolRepositories;
    }

    @Override
    public List<Rol> listar(){
        return rolRepositories.findAll();
    }

    @Override
    public Rol guardar(Rol rol){
        return rolRepositories.save(rol);
    }

    @Override
    public void eliminar(Integer id){
        rolRepositories.deleteById(id);
    }

    @Override
    public Rol buscarPorId(Integer id){
        return rolRepositories.findById(id).orElse(null);
    }

    @Override
    public List<Rol> buscarPorNombre(String nomRol){
        return rolRepositories.findByNomRol(nomRol);
    }

    //Service Implementacion, Va la logina que conecta el controoller con la BD
}

