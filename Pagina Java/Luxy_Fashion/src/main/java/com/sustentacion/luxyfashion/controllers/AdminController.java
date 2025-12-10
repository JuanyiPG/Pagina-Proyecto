package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Usuario;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin")
public class AdminController {

    @GetMapping("/index")//el httpsesion es para comprobar el registro
    public String adminIndex(HttpSession session) {

        Usuario u = (Usuario) session.getAttribute("usuarioLogueado");

        if (u == null || !u.getRol().equals("ADMIN")) {
            return "redirect:/login";
        }

        return "admin/indexadmin"; // tu vista admin
    }
}
