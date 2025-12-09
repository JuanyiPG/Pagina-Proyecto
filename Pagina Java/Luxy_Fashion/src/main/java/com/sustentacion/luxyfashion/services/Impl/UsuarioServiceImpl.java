package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import com.sustentacion.luxyfashion.services.UsuarioService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class UsuarioServiceImpl implements UsuarioService, UserDetailsService {

    private final UsuarioRepositories usuarioRepositories;
    private final PasswordEncoder passwordEncoder;

    public UsuarioServiceImpl(UsuarioRepositories usuarioRepositories, PasswordEncoder passwordEncoder) {
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
        usuario.setContraseña(passwordEncoder.encode(usuario.getContraseña()));
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

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Usuario usuario = usuarioRepositories.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("Usuario no encontrado"));

        return User.builder()
                .username(usuario.getUsername())
                .password(usuario.getContraseña())
                .roles(usuario.getRol())
                .build();
    }

    public Usuario autenticar(String username, String contraseña) {
        Usuario usuario = usuarioRepositories.findByUsername(username)
                .orElseThrow(() -> new IllegalArgumentException("El usuario no existe"));

        if (!passwordEncoder.matches(contraseña, usuario.getContraseña())) {
            throw new IllegalArgumentException("Contraseña incorrecta");
        }
        return usuario;
    }
}
