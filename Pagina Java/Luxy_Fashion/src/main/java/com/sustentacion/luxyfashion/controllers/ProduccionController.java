package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Produccion;
import com.sustentacion.luxyfashion.services.ProduccionService;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.PedidoService;
import com.sustentacion.luxyfashion.services.MateriaPrimaService;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/emple/produccion")
public class ProduccionController {

    private final ProduccionService produccionService;
    private final EmpleService empleService;
    private final PedidoService pedidoService;
    private final MateriaPrimaService materiaPrimaService;

    public ProduccionController(ProduccionService produccionService,
                                EmpleService empleService,
                                PedidoService pedidoService,
                                MateriaPrimaService materiaPrimaService) {
        this.produccionService = produccionService;
        this.empleService = empleService;
        this.pedidoService = pedidoService;
        this.materiaPrimaService = materiaPrimaService;
    }

    // LISTAR

    @GetMapping()
    public String listar(Model model) {

        List<Produccion> producciones = produccionService.listar();

        model.addAttribute("producciones", producciones);
        model.addAttribute("produccion", new Produccion());

        model.addAttribute("empleados", empleService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "empleado/produccion/indexproduccion";
    }

    // NUEVO

    @GetMapping("/nuevo")
    public String nuevo(Model model) {

        model.addAttribute("produccion", new Produccion());
        model.addAttribute("empleados", empleService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "empleado/produccion/indexproduccion";
    }

    // GUARDAR

    @PostMapping("/guardar")
    public String guardar(Produccion produccion) {
        produccionService.guardar(produccion);
        return "redirect:/emple/produccion?success=true";
    }

    // EDITAR

    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {

        Produccion produccion = produccionService.buscarPorId(id);

        if (produccion == null) {
            return "redirect:/emple/produccion?error=not_found";
        }

        model.addAttribute("produccion", produccion);
        model.addAttribute("empleados", empleService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "empleado/produccion/editarProduccion";
    }


    // BUSCAR

    @GetMapping("/buscar")
    public String buscar(
            @RequestParam(name = "buscar", required = false) String filtro,
            Model model) {

        List<Produccion> producciones;

        if (filtro == null || filtro.isEmpty()) {
            producciones = produccionService.listar();
        } else {
            producciones = produccionService.buscarvarioscampos(filtro);
        }

        model.addAttribute("producciones", producciones);
        model.addAttribute("produccion", new Produccion());
        model.addAttribute("empleados", empleService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "empleado/produccion/indexproduccion";
    }

    // ELIMINAR

    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        produccionService.eliminar(id);
        return "redirect:/emple/produccion?deleted=true";
    }

    // VISTA ADMIN

    @GetMapping("/admin")
    public String listarAdmin(Model model) {

        List<Produccion> producciones = produccionService.listar();

        model.addAttribute("producciones", producciones);
        model.addAttribute("produccion", new Produccion());

        model.addAttribute("empleados", empleService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "admin/listproduccion/indexproduccion";
    }

    @GetMapping("/editarAdmin/{id}")
    public String editarAdmin(@PathVariable Integer id, Model model) {

        Produccion produccion = produccionService.buscarPorId(id);

        if (produccion == null) {
            return "redirect:/emple/produccion?error=not_found";
        }

        model.addAttribute("produccion", produccion);
        model.addAttribute("empleados", empleService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "admin/listproduccion/editarProduccion";
    }

    @PostMapping("/guardarAdmin")
    public String guardarAdmin(Produccion produccion) {
        produccionService.guardar(produccion);
        return "redirect:/emple/produccion/admin?success=true";
    }

    @GetMapping("/eliminarAdmin/{id}")
    public String eliminarAdmin(@PathVariable Integer id) {
        produccionService.eliminar(id);
        return "redirect:/emple/produccion/admin?deleted=true";
    }
}

