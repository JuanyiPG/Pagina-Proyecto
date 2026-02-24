package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.services.RolService;
import com.sustentacion.luxyfashion.services.UsuarioService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/login")
public class UsuarioController {

    private final UsuarioService usuarioService;
    private final RolService rolService;

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
        this.rolService = rolService;
    }

    @GetMapping()
    public String mostrarLogin(@ModelAttribute Cliente cliente) {

        Rol rol = RolService("CLIENTE").get(1);
        model.addAttribute("cliente", new Cliente());

        return "login/loginRegistro";
    }
}
