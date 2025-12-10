package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Usuario;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
    @GetMapping("/")
    public String home() {
        return "index"; // plantilla en templates
    }

    @GetMapping("/admin")//el httpsesion es para comprobar el registro
    public String adminIndex(HttpSession session) {
        return "admin/indexadmin"; // tu vista admin
    }
}
