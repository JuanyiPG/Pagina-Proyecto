package com.sustentacion.luxyfashion.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
    @GetMapping
    public String MostrarForm(){
        return "index";
    }
}
