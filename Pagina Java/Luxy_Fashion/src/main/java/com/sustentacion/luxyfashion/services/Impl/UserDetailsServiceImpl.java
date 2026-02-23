package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import org.springframework.security.core.userdetails.*;
import org.springframework.stereotype.Service;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    private final UsuarioRepositories usuarioRepositories;

    public UserDetailsServiceImpl(UsuarioRepositories usuarioRepositories) {
        this.usuarioRepositories = usuarioRepositories;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {

        Usuario usuario = usuarioRepositories.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("Usuario no encontrado"));

        String rol = usuario.getRol().getNomRol();

        return User.builder()
                .username(usuario.getUsername())
                .password(usuario.getContrasena())
                .roles(rol)
                .build();
    }
}
