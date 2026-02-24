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

    @GetMapping("/productoCliente")
    public String producto(){
        return "cliente/pedido";
    }

    @GetMapping("/err")
    public String err(){
        return "error/404";
    }

    @GetMapping("/registro")
    public String registro() {
        return "index"; // plantilla en templates
    }

}
