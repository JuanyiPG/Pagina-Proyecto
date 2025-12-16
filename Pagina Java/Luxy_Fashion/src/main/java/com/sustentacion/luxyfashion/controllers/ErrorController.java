package com.sustentacion.luxyfashion.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class ErrorController implements org.springframework.boot.web.servlet.error.ErrorController {

    @RequestMapping("/error")
    public String handleError() {
        // Aquí puedes poner lógica personalizada, como registrar el error o mostrar un mensaje amigable
        return "error/404"; // Nombre de la vista de error (ej., error.html)
    }
}

