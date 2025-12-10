package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Usuario;
import org.springframework.stereotype.Service;

import java.util.List;


public interface UsuarioService {
    List<Usuario> ListarOrdenAsc();
    List<Usuario> BucarVariosCampos(String filtro);
    List<Usuario> listar();
    Usuario guardar(Usuario usuario);
    void EliminarPorId(Integer id);
    Usuario BuscarPorId(Integer id);
    void validarUsuario (String username);
    Usuario autenticar(String username, String contraseña);




}
