package com.sustentacion.luxyfashion.controllers;

//Pide cosas, recive la peticion.

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.repositories.RolRepositories;
import com.sustentacion.luxyfashion.services.RolService;

import java.util.List;

    //@RestController, sirve para devolver en Json
    @Controller //Nos sirve para devolver un Documento html
    @RequestMapping("/roles")
    public class RolController {


        private final RolService rolService;

        public RolController(RolService rolService) {
            this.rolService = rolService;
        }

        //Es el que maneja las solicitudes, ejecutando el metodo que corresponde.

        @GetMapping()
        public String listarOrdenados(Model model) {
            List<Rol> roles = rolService.listarRolesOrdenados();
            model.addAttribute("roles", roles); //La lista
            model.addAttribute("rol", new Rol()); //Para el formulario
            return "roles/ROL_INDEX";
        }

        @GetMapping("/nuevo")
        public String nuevo(Model model) {
            model.addAttribute("rol", new Rol());
            return "roles/ROL_INDEX";
        }

        //responder petidiones post, para formularios o crear registros
        @PostMapping("/guardar")
        public String guardar(Rol rol) {
            rolService.guardar(rol);
            return "redirect:/roles?success=true";
        }

        @GetMapping("/editar/{id}")
        public String editar(@PathVariable Integer id, Model model) {
            Rol rol = rolService.buscarPorId(id);

            if (rol == null){
                return "redirect:/roles?error=not_found";
            }
            List<Rol> listarRoles = rolService.listarRolesOrdenados();
            model.addAttribute("roles", listarRoles);
            model.addAttribute("rol", rol);
            return "roles/EDITAR_ROL"; //<- aqui se direcciona a que html va
        }

        // Eliminar
        @GetMapping("/eliminar/{id}")
        public String eliminar(@PathVariable Integer id) {
            rolService.eliminar(id);
            return "redirect:/roles";
        }

        //Controla las URLs y conecta la vista con el servicio

        //GET = ver
        //
        //POST = crear
        //
        //PUT = reemplazar todo
        //
        //PATCH = actualizar un pedazo
        //
        //DELETE = borrar

    }
