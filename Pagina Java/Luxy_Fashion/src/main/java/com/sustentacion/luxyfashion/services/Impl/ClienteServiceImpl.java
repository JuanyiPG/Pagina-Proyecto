package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.ClienteRepositories;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import com.sustentacion.luxyfashion.services.ClienteService;
import com.sustentacion.luxyfashion.services.RolService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
@Transactional
@Service
public class ClienteServiceImpl implements ClienteService {

        private final ClienteRepositories clienteRepositories;

        public ClienteServiceImpl(ClienteRepositories clienteRepositories,
                                  UsuarioRepositories usuarioRepositories,
                                  RolService rolService) {
            this.clienteRepositories = clienteRepositories;
        }

    @Override
    public List<Cliente> listar(){
         return clienteRepositories.findAll();
    }

    @Override
    public Cliente registrarCliente(Cliente cliente) {
        return null;
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
    public void eliminarClienteUsuario(Integer id){
         clienteRepositories.deleteById(id);
    }

    @Override
    public Cliente BuscarPorId(Integer id){
         return clienteRepositories.findById(id).orElse(null);
    }

    @Override
    public void guardar(Cliente cliente) {
        clienteRepositories.save(cliente);
    }
}
