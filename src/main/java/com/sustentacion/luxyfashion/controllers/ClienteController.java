package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.services.ClienteService;
import com.sustentacion.luxyfashion.services.RolService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/cliente")
public class ClienteController {
    private final ClienteService clienteService;
    private RolService rolService;
    //Aqui no inyectamos el service usuario ya que ya lo hicimos en el service Cliente

    public ClienteController(RolService rolService, ClienteService clienteService ){
        this.clienteService = clienteService;
        this.rolService = rolService;
    }

    @GetMapping()
    public String index(Model model){
        List<Cliente> clientes = clienteService.listarOrdenAsc();
        model.addAttribute("clientes", clientes);
        model.addAttribute("cliente", new Cliente());
        model.addAttribute("roles", rolService.listar());

        return "login/LoginRegistro";
    }

    @GetMapping("/nuevo") //mostrar el formulario vacio
    public String nuevo(Model model){
        model.addAttribute("clientes", new Cliente());
        return "login/LoginRegistro";
    }

    @PostMapping("/registar") //guardar   //modelAtribute, trae los datos del formulario y los llena autoamtic
    public String registrarCliente(@ModelAttribute Cliente cliente, Model model) {
        // Buscar el rol CLIENTE
        List<Rol> roles = rolService.buscarPorNombre("CLIENTE");

        if (roles.isEmpty()) {
            throw new IllegalArgumentException("No existe el rol CLIENTE");
        }

        Rol rolSeleccionado = roles.get(0); // ← ahora sí es un Rol
        cliente.setRol(rolSeleccionado);
        // Asignar el rol automáticamente
        cliente.setRol(rolSeleccionado); //Un objeto Rol que represneta cliente
        try {
            clienteService.guardarClienteUsuario(cliente);
            return "redirect:/cliente"; // o la página de bienvenida
        } catch (IllegalArgumentException e) {
            // Mostrar mensaje de error en el formulario
            model.addAttribute("error", e.getMessage());
            model.addAttribute("cliente", cliente);
            return "login/LoginRegistro"; // vuelve al formulario con mensaje
        }
    }

    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model){
        Cliente cliente = clienteService.BuscarPorId(id);
        if (cliente == null){
            return "redirect:/empleado?error=not_found";
        }
        model.addAttribute("cliente", cliente);
        return "login/editar";
    }

    @GetMapping("/buscar")
    public String buscar(@RequestParam(name = "buscar", required = false) String filtro, Model model){
        List<Cliente> clientes;
        List<Empleado> empleados;

        if (filtro == null || filtro.isEmpty()){
            clientes = clienteService.listar();
            model.addAttribute("clientes", clientes);
        }else {
            clientes = clienteService.buscarVariosCampos(filtro);
            model.addAttribute("clientes", clientes);
        }
        model.addAttribute("cliente", new Cliente());
        model.addAttribute("roles", rolService.listar());
        return "";
    }
}
