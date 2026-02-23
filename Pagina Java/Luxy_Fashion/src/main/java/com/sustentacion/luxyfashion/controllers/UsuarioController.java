package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.services.UsuarioService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/login")
public class UsuarioController {

    private final UsuarioService usuarioService;

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping()
    public String mostrarLogin(Model model) {

        model.addAttribute("cliente", new Cliente());

        return "login/loginRegistro";
    }
}
