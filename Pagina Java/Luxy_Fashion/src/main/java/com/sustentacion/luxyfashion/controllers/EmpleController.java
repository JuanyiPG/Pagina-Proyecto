package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.RolService;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@Controller
@RequestMapping("/admin/empleado")
public class EmpleController {

    private final RolService rolService;
    private final EmpleService empleService;

    public EmpleController ( RolService rolService,EmpleService empleService){
        this.empleService = empleService;
        this.rolService = rolService;
    }



    @GetMapping()
    public String listarOrdenados(Model model){
        List<Empleado> empleados = empleService.listarEmpleadosOrdenados();
        model.addAttribute("empleados", empleados);
        model.addAttribute("empleado", new Empleado());
        model.addAttribute("roles", rolService.listar());

        return "admin/empleado/emple_index";
    }

    @GetMapping("/index")
    public String empleadoIndex(HttpSession session) {
        Usuario u = (Usuario) session.getAttribute("usuarioLogueado");
        if (u == null || !u.getRol().equals("EMPLEADO")) {
            return "redirect:/login"; // Si no es empleado o no está logueado
        }
        return "empleado/indexemple"; // Vista de empleado
    }

    @GetMapping("/admin/nuevo")
    public String nuevo(Model model){
        Empleado empleado = new Empleado();
        empleado.setRol(new Rol()); // <-- Aquí está la magia

        model.addAttribute("empleado", empleado);
        model.addAttribute("roles", rolService.listar()); // <-- Lo necesitas para llenar el select
        return "admin/empleado/emple_index";
    }

    @PostMapping("/guardar")
    public String guardar(Empleado empleado){
        //Asignar el rol
        System.out.println("Rol enviado:");
        System.out.println("objeto rol: " + empleado.getRol());
        System.out.println("id del rol: " + empleado.getRol().getId_rol());
        Rol rolSeleccionado = rolService.buscarPorId(empleado.getRol().getId_rol());
        empleado.setRol(rolSeleccionado);
        empleService.guardar(empleado);
        return "redirect:/admin/empleado?success=true";
    }

    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model){
        Empleado empleado = empleService.buscarPorId(id);
        if (empleado == null){
            return "redirect:empleado?error=not_found";
        }
        model.addAttribute("empleado", empleado);
        return "admin/empleado/editar_emple";
    }

    @GetMapping("/buscar")
    public String buscar(@RequestParam (name="buscar", required = false) String filtro, Model model){
        List<Empleado> empleados;

        if (filtro == null || filtro.isEmpty()){
            empleados = empleService.listar();
            model.addAttribute("empleados", empleados);
        }else {
            empleados = empleService.buscarVariosCampos(filtro);
            model.addAttribute("empleados", empleados);
        }
        model.addAttribute("empleado", new Empleado());
        model.addAttribute("roles", rolService.listar());
        return "admin/empleado/emple_index";
    }

        @GetMapping("/eliminar/{id}")
        public String eliminar(@PathVariable Integer id) {
            empleService.eliminar(id);
            return "redirect:/admin/empleado?error=not_found";
        }


    }
