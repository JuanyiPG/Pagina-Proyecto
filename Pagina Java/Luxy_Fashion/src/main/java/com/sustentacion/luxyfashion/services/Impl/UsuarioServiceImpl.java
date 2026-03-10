package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import com.sustentacion.luxyfashion.services.UsuarioService;
import jakarta.transaction.Transactional;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class UsuarioServiceImpl implements UsuarioService {

    private final UsuarioRepositories usuarioRepositories;
    private final PasswordEncoder passwordEncoder;

    public UsuarioServiceImpl(
            UsuarioRepositories usuarioRepositories,
            PasswordEncoder passwordEncoder) {

        this.usuarioRepositories = usuarioRepositories;
        this.passwordEncoder = passwordEncoder;
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

        String passwordCifrada =
                passwordEncoder.encode(usuario.getContrasena());

        usuario.setContrasena(passwordCifrada);

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
}
