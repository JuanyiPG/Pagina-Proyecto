package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.services.UsuarioService;
import jakarta.servlet.http.HttpSession;
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

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping()
    public String mostrarLogin() {
        return "/admin/cliente"; // tu vista login.html
    }

    @PostMapping
    public String login(@RequestParam String username,
                        @RequestParam String contrasena,
                        HttpSession session,
                        Model model) {

        try {
            Usuario u = usuarioService.autenticar(username, contrasena);

            session.setAttribute("usuarioLogueado", u);

            switch (u.getRol()) {

                case "ADMIN":
                    return "redirect:/admin/admin";  // tu home de admin

                case "EMPLEADO":
                    return "redirect:/admin/empleado/index"; // home empleado

                case "CLIENTE":
                    return "redirect:/admin/admin"; // home cliente

                default:
                    model.addAttribute("error", "Rol no reconocido");
                    return "login/loginRegistro";
            }

        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
            return "login/loginRegistro";
        }
    }
}
