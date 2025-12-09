package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.services.ClienteService;
import com.sustentacion.luxyfashion.services.RolService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.List;

@Controller
@RequestMapping("/cliente")
public class ClienteController {

    private final ClienteService clienteService;
    private final RolService rolService;
    private final PasswordEncoder passwordEncoder;

    public ClienteController(RolService rolService, ClienteService clienteService,PasswordEncoder passwordEncoder ){
        this.clienteService = clienteService;
        this.rolService = rolService;
        this.passwordEncoder = passwordEncoder;
    }

    // LISTA DE CLIENTES (esta NO es la vista de registro)
    @GetMapping()
    public String index(Model model){
        List<Cliente> clientes = clienteService.listarOrdenAsc();
        model.addAttribute("clientes", clientes);
        return "cliente/indexcliente"; // Vista correcta para listar
    }

    // MOSTRAR FORMULARIO DE REGISTRO
    @GetMapping("/nuevo")
    public String mostrarFormulario(Model model) {
        model.addAttribute("cliente", new Cliente());
        return "login/LoginRegistro";
    }

    @PostMapping("/registrar")
    public String registrarCliente(@ModelAttribute Cliente cliente, Model model) {
        try {
            clienteService.registrarCliente(cliente);
            return "redirect:/login?registrado"; // exito
        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
            model.addAttribute("cliente", cliente);
            return "login/LoginRegistro";
        }
    }

    // EDITAR CLIENTE
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model){
        Cliente cliente = clienteService.BuscarPorId(id);
        if (cliente == null){
            return "redirect:/cliente?error=not_found";
        }
        model.addAttribute("cliente", cliente);
        return "login/editar";
    }

    // BUSCAR CLIENTES
    @GetMapping("/buscar")
    public String buscar(@RequestParam(name = "buscar", required = false) String filtro, Model model){
        List<Cliente> clientes;

        if (filtro == null || filtro.isEmpty()){
            clientes = clienteService.listar();
        } else {
            clientes = clienteService.buscarVariosCampos(filtro);
        }

        model.addAttribute("clientes", clientes);
        return "cliente/indexcliente";
    }
}
