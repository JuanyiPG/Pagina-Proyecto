package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.ClienteRepositories;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import com.sustentacion.luxyfashion.services.ClienteService;
import com.sustentacion.luxyfashion.services.RolService;
import jakarta.transaction.Transactional;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class ClienteServiceImpl implements ClienteService {

        private final ClienteRepositories clienteRepositories;
        private final UsuarioRepositories usuarioRepositories;
        private final PasswordEncoder passwordEncoder;
        private final RolService rolService;

        public ClienteServiceImpl(ClienteRepositories clienteRepositories,
                                  UsuarioRepositories usuarioRepositories,
                                  PasswordEncoder passwordEncoder,
                                  RolService rolService) {
            this.clienteRepositories = clienteRepositories;
            this.usuarioRepositories = usuarioRepositories;
            this.passwordEncoder = passwordEncoder;
            this.rolService = rolService;
        }

        @Override
        public Cliente registrarCliente(Cliente cliente) {

            if (clienteRepositories.existsByCorreo(cliente.getCorreo()))
                throw new IllegalArgumentException("Correo ya registrado");

            if (clienteRepositories.existsByUsuario(cliente.getUsuario()))
                throw new IllegalArgumentException("Usuario ya en uso");

            // Buscar rol CLIENTE
            Rol rol = rolService.buscarPorNombre("Cliente").get(0);
            cliente.setRol(rol);

            // Encriptar contraseña
            cliente.setContra_clien(passwordEncoder.encode(cliente.getContra_clien()));

            // Guardar cliente
            Cliente clienteGuardado = clienteRepositories.save(cliente);

            // Crear usuario para Spring Security
            Usuario usuario = new Usuario();
            usuario.setUsername(cliente.getUsuario());
            usuario.setContraseña(cliente.getContra_clien());
            usuario.setRol("CLIENTE");
            usuario.setCliente(clienteGuardado);
            usuarioRepositories.save(usuario);

            return clienteGuardado;
        }

    @Override
    public List<Cliente> listar(){
         return clienteRepositories.findAll();
    }
    @Override
    public List<Cliente> listarOrdenAsc(){
         return clienteRepositories.findAllByOrderByNomClienAsc();
    }

    @Override
    public List<Cliente> buscarVariosCampos(String filtro){
         return clienteRepositories.buscarVariosCampos(filtro);
    }

    @Override
    public Cliente guardarClienteUsuario(Cliente cliente){

        // validar correo
        if (clienteRepositories.existsByCorreo(cliente.getCorreo())){
            throw new IllegalArgumentException("El correo que ingresaste ya está registrado");
        }

        // validar usuario
        if (clienteRepositories.existsByUsuario(cliente.getUsuario())){
            throw new IllegalArgumentException("El nombre de usuario ya está en uso");
        }

        return clienteRepositories.save(cliente);
    }

    @Override
    public void eliminarClienteUsuario(Integer id){
         clienteRepositories.deleteById(id);
    }

    @Override
    public Cliente BuscarPorId(Integer id){
         return clienteRepositories.findById(id).orElse(null);
    }
}
