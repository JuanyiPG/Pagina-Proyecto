package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.repositories.ClienteRepositories;
import com.sustentacion.luxyfashion.services.ClienteService;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class ClienteServiceImpl implements ClienteService {
    private final ClienteRepositories clienteRepositories;
    public ClienteServiceImpl (ClienteRepositories clienteRepositories){
        this.clienteRepositories = clienteRepositories;
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
        //validar correo
        if (clienteRepositories.existsByCorreo(cliente.getCorreo())){
            throw new IllegalArgumentException("El correo que ingresaste ya esta registrado ");
            //Significa, lanza esta exepcion con el siguiente mensaje cuando encuentres el error.
        }

        //validar nombre de usuario

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
