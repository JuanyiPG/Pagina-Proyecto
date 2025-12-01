package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.repositories.RolRepositories;
import org.springframework.stereotype.Service;
import com.sustentacion.luxyfashion.models.Rol;

import java.util.List;

@Service
class RolServiceImpl implements RolService {
    private final RolRepositories rolRepositories;

    //Una inyeccion es darle a la clase un objeto sin que la tenga que crear con new.

    //Inyeccion por Constructor: Se entrega la dependencia al crear el objeto, garantizando que siempre esté lista y no sea null
    public RolServiceImpl(RolRepositories rolRepositories){
        this.rolRepositories = rolRepositories;
    }

    @Override
    public List<Rol> listarRolesOrdenados(){
        return rolRepositories.findAllByOrderByNomRolAsc();
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

    //Service Implementacion, Va la logina que conecta el controoller con la BD
}

