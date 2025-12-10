package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.services.ClienteService;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/cliente")
public class ClienteController {

    private final ClienteService clienteService;

    public ClienteController(ClienteService clienteService) {
        this.clienteService = clienteService;
    }

    // Mostrar lista de clientes
    @GetMapping()
    public String listarClientes(Model model) {
        List<Cliente> clientes = clienteService.listar();
        model.addAttribute("clientes", clientes);
        model.addAttribute("cliente", new Cliente());
        return "login/loginRegistro"; // tu plantilla Thymeleaf
    }

    @GetMapping("/index")
    public String clienteIndex(HttpSession session) {
        Usuario u = (Usuario) session.getAttribute("usuarioLogueado");

        if (u == null || !u.getRol().equals("CLIENTE")) {
            return "redirect:/login";
        }
        return "cliente/indexcliente";
    }

    // Mostrar formulario para nuevo cliente
    @GetMapping("/nuevo")
    public String nuevoCliente(Model model) {
        model.addAttribute("cliente", new Cliente());
        return "login/loginRegistro"; // tu plantilla de formulario
    }

    // Guardar cliente (nuevo o editar)
    @PostMapping("/guardar")
    public String guardarCliente(@ModelAttribute Cliente cliente, Model model) {
        try {
            if (cliente.getId_clien() == null) {
                clienteService.registrarCliente(cliente); // registro con usuario
            } else {
                clienteService.guardar(cliente); // edición simple
            }
            return "redirect:/admin/cliente";
        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
            model.addAttribute("cliente", cliente);
            return "login/loginRegistro";
        }
    }

    // Editar cliente
    @GetMapping("/editar/{id}")
    public String editarCliente(@PathVariable Integer id, Model model) {
        Cliente cliente = clienteService.BuscarPorId(id);
        if (cliente == null) {
            return "redirect:/admin/cliente";
        }
        model.addAttribute("cliente", cliente);
        return "login/loginRegistro";
    }

    // Eliminar cliente
    @GetMapping("/eliminar/{id}")
    public String eliminarCliente(@PathVariable Integer id) {
        clienteService.eliminarClienteUsuario(id);
        return "redirect:/admin/cliente";
    }

    // Buscar clientes por filtro (opcional)
    @GetMapping("/buscar")
    public String buscarClientes(@RequestParam String filtro, Model model) {
        List<Cliente> clientes = clienteService.buscarVariosCampos(filtro);
        model.addAttribute("clientes", clientes);
        return "login/loginRegistro";
    }
}
