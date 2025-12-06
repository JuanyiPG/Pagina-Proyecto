package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import org.springframework.stereotype.Service;

import java.util.List;


public interface EmpleService {
    List<Empleado> listarEmpleadosOrdenados();
    Empleado guardar(Empleado empleado);
    void eliminar(Integer id);
    Empleado buscarPorId(Integer id);
    List<Empleado> buscarVariosCampos(String filtro);
    List<Empleado> listar();
}
