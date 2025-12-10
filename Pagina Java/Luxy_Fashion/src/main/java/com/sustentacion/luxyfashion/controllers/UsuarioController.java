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
        return "login/loginRegistro"; // tu vista login.html
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
                    return "redirect:admin/index";  // tu home de admin

                case "EMPLEADO":
// home empleado
                    return "redirect:admin/empleado/index"; // home empleado


                case "CLIENTE":
                    return "redirect:/admin/cliente/index"; // home cliente

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
