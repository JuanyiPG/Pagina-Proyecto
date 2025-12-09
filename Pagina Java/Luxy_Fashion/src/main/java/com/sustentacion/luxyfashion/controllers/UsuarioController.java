package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
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

    // GET para mostrar login + registro
    @GetMapping
    public String mostrarLogin(Model model) {
        model.addAttribute("cliente", new Cliente()); // Para el registro
        return "Login/LoginRegistro"; // Vista que combina login y registro
    }

    // GET para redirigir después del login según rol
    //usamos el seguriti para comprobar sus roles, con esto nos ayuda a reducir el codigo
    @GetMapping("/default")
    public String redirectAfterLogin(org.springframework.security.core.Authentication authentication) {
        String role = authentication.getAuthorities().iterator().next().getAuthority();

        switch (role) {
            case "ROLE_ADMIN":
                return "redirect:/admin/dashboard";
            case "ROLE_EMPLEADO":
                return "redirect:/empleado/dashboard";
            case "ROLE_CLIENTE":
                return "redirect:/cliente";
            default:
                return "redirect:/login?error";
        }
    }
}



