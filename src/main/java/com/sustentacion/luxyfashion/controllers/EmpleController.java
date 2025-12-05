package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.RolService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@Controller
@RequestMapping("/empleado")
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

        return "empleado/emple_index";
    }

    @GetMapping("/nuevo") //mostrar el formulario vacio
    public String nuevo(Model model){
        model.addAttribute("empleado", new Empleado());
        return "empleado/emple_index";
    }

    @PostMapping("/guardar")
    public String guardar(Empleado empleado){
        //Asignar el rol
        Rol rolSeleccionado = rolService.buscarPorId(empleado.getRol().getId_rol());
        empleado.setRol(rolSeleccionado);
        empleService.guardar(empleado);
        return "redirect:/empleado?success=true";
    }

    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model){
        Empleado empleado = empleService.buscarPorId(id);
        if (empleado == null){
            return "redirect:/empleado?error=not_found";
        }
        model.addAttribute("empleado", empleado);
        return "empleado/editar_emple";
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
        return "empleado/emple_index";
    }



}
