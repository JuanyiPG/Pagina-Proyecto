package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import com.sustentacion.luxyfashion.services.UsuarioService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class UsuarioServiceImpl implements UsuarioService {

    private final UsuarioRepositories usuarioRepositories;

    public UsuarioServiceImpl(UsuarioRepositories usuarioRepositories) {
        this.usuarioRepositories = usuarioRepositories;
    }

    @Override
    public List<Usuario> ListarOrdenAsc() {
        return usuarioRepositories.findAllByOrderByUsername();
    }

    @Override
    public List<Usuario> BucarVariosCampos(String filtro) {
        return usuarioRepositories.buscarVariosCampos(filtro);
    }

    @Override
    public List<Usuario> listar() {
        return usuarioRepositories.findAll();
    }

    @Override
    public Usuario guardar(Usuario usuario) {
        return usuarioRepositories.save(usuario);
    }

    @Override
    public void EliminarPorId(Integer id) {
        usuarioRepositories.deleteById(id);
    }

    @Override
    public Usuario BuscarPorId(Integer id) {
        return usuarioRepositories.findById(id).orElse(null);
    }

    @Override
    public void validarUsuario(String username) {
        if (usuarioRepositories.existsByUsername(username))
            throw new IllegalArgumentException("Ese nombre de usuario ya existe");
    }

    public Usuario autenticar(String username, String contraseña) {
        Usuario usuario = usuarioRepositories.findByUsername(username)
                .orElse(null);

        if (usuario == null) {
            throw new IllegalArgumentException("El usuario no existe");
        }

        if (!usuario.getContrasena().equals(contraseña)) {
            throw new IllegalArgumentException("Contraseña incorrecta");
        }

        return usuario;
    }

}
