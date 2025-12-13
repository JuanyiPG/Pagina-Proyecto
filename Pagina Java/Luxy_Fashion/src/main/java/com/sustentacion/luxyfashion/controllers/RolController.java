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
    @RequestMapping("/admin/roles")
    public class RolController {

        private final RolService rolService;

        //Constructor, el cual instancia la inyeccion y la conexion entre capas.
        public RolController(RolService rolService) {
            this.rolService = rolService;
        }

        @GetMapping()
        public String index(Model model){ //model sirve para enviar los datos al html
            model.addAttribute("rol", new Rol()); // ← ESTO HACE FALTA
            model.addAttribute("roles", rolService.listar()); // si tienes tabla
            return "admin/roles/ROL_INDEX";
        }

        @GetMapping("/nuevo")
        public String nuevo(Model model) {
            model.addAttribute("rol", new Rol());
            return "admin/roles/ROL_INDEX";
        }

        //responder petidiones post, para formularios o crear registros
        @PostMapping("/guardar")
        public String guardar(Rol rol) {
            rolService.guardar(rol);
            return "redirect:/admin/roles?success=true";
        }

        @GetMapping("/editar/{id}") //Path se usa para traer los datos del formulario
        public String editar(@PathVariable Integer id, Model model) { //el Path ayuda a direccionar el metodo y saber cual se debe de editar
            Rol rol = rolService.buscarPorId(id);
             if (rol == null){
                 return "redirect:/admin/roles?error=not_found";
             }
            model.addAttribute("rol", rol);
            return "admin/roles/EDITAR_ROL"; //<- aqui se direcciona a que html va
        }
/*Diferencia simple entre ambos
        @PathVariable	parte de la URL	/editar/10
        @RequestParam	parte de los parámetros	/buscar?texto=rol
 */
        //Buscar
        @GetMapping("/buscar")
        public String buscar(@RequestParam (name = "nomRol", required = false)String nomRol, Model model){
                                           //El name se usa para indicar el nombre en el formulario
            List<Rol> roles;

            // Siempre enviar un objeto rol porque la vista lo necesita
            model.addAttribute("rol", new Rol());

            if (nomRol == null || nomRol.isEmpty()) {
                roles = rolService.listar();
            }else {
                roles = rolService.buscarPorNombre(nomRol);
            }
            model.addAttribute("roles", roles);
            model.addAttribute("rol", new Rol());
            return "admin/roles/ROL_INDEX";
        }


        // Eliminar
        @GetMapping("/eliminar/{id}")
        public String eliminar(@PathVariable Integer id) {
            rolService.eliminar(id);
            return "redirect:/admin/roles?error=not_found";
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
