package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.RolService;
import com.sustentacion.luxyfashion.services.UsuarioService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/login")
public class UsuarioController {
    private final UsuarioService usuarioService;

    public UsuarioController ( UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }
    @GetMapping()
    public String mostrarLogin() {
        return "Login/LoginRegistro";
    }

    @PostMapping("/login")
    public String procesarLogin(@RequestParam String username,
                                @RequestParam String contraseña,
                                Model model) {


        usuarioService.autenticar(username, contraseña);

        if (usuarioService == null) {
            model.addAttribute("error", "Usuario o contraseña incorrectos");
            return "login";
        }

        return "redirect:/login";
    }
}

