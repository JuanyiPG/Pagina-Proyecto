package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.repositories.EmpleRepositories;
import com.sustentacion.luxyfashion.services.EmpleService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EmpleServiceImpl implements EmpleService {
private final EmpleRepositories empleRepositories;

public EmpleServiceImpl (EmpleRepositories empleRepositories){
    this.empleRepositories = empleRepositories;
}

@Override
public List<Empleado> listar(){
    return empleRepositories.findAll();
}
@Override
    public List<Empleado> listarEmpleadosOrdenados(){
    return empleRepositories.findAllByOrderByNomEmpleAsc();
    }

    @Override
    public Empleado guardar(Empleado empleado){
    return empleRepositories.save(empleado);
    }

    @Override
    public void eliminar(Integer id){
    empleRepositories.deleteById(id);
    }

    @Override
    public Empleado buscarPorId(Integer id){
    return empleRepositories.findById(id).orElse(null);
    }

    @Override
    public List<Empleado>buscarVariosCampos(String filtro){
    return empleRepositories.buscarVariosCampos(filtro);
    }
}
