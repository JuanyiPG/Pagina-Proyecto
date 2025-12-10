package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.RolService;
import com.sustentacion.luxyfashion.services.UsuarioService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/login")
public class UsuarioController {
    @Autowired
    private UsuarioService usuarioService;

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping("/login")
    public String formLogin() {
        return "login"; // tu página de login
    }

    @PostMapping("/login")
    public String login(@RequestParam String username,
                        @RequestParam String contraseña,
                        HttpSession session,
                        Model model) {

        try {
            Usuario u = usuarioService.autenticar(username, contraseña);

            session.setAttribute("usuarioLogueado", u);

            switch (u.getRol()) {

                case "ADMIN":
                    return "redirect:/admin/index";

                case "EMPLEADO":
                    return "redirect:/empleado/index";

                case "CLIENTE":
                    return "redirect:/cliente/index";

                default:
                    model.addAttribute("error", "Rol no reconocido");
                    return "login";
            }

        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
            return "login";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/auth/login";
    }

}



