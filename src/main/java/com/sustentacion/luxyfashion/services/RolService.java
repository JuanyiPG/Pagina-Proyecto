package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Rol;

import java.util.List;

//El service va la logica del negicio, resive la peticion del controller
public interface RolService {
    List<Rol> listar();
    Rol guardar(Rol rol);
    void eliminar(Integer id);
    Rol buscarPorId(Integer id);
}

//Define que cosas pueden hacer un servicio de roles
//Service es la interfaz, la conexion del usuario y el sistema

