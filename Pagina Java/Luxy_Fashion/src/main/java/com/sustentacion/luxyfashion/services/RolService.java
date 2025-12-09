package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Rol;
import org.springframework.stereotype.Service;

import java.util.List;

//Solo declara metodos
//El service va la logica del negicio, resive la peticion del controller

public interface RolService {
    List<Rol> buscarPorNombre(String nomRol);
    Rol guardar(Rol rol);
    void eliminar(Integer id);
    Rol buscarPorId(Integer id);
    List<Rol> listar ();
}

//Define que cosas pueden hacer un servicio de roles
//Service es la interfaz, la conexion del usuario y el sistema

