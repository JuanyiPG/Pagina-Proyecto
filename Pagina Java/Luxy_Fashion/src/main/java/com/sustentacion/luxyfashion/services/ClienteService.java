package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.stereotype.Service;

import java.util.List;


public interface ClienteService {
    Cliente registrarCliente(Cliente cliente);
    List<Cliente> listarOrdenAsc(); //Estos si se exponen ya que son consultas copletas/ grandes.
    List<Cliente> buscarVariosCampos(String filtro);
    List<Cliente> listar();
    //En el services no llamamos o exponemos consulatas pequeñas, en ese caso la bsuqueda para el
    //el correo, ya que es al hacerlo podemos arruinar la logica del sistema, entonces solo se llama desde el
    //serviceImpl sin declarar/exponerla aca.


    void eliminarClienteUsuario(Integer id);
    Cliente BuscarPorId(Integer id);


    void guardar(Cliente cliente);
}
