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
@RequestMapping("/produccion")
public class ProduccionController {

    private final ProduccionService produccionService;
    private final EmpleService empleadoService;
    private final PedidoService pedidoService;
    private final MateriaPrimaService materiaPrimaService;

    public ProduccionController(
            ProduccionService produccionService,
            EmpleService empleadoService,
            PedidoService pedidoService,
            MateriaPrimaService materiaPrimaService) {

        this.produccionService = produccionService;
        this.empleadoService = empleadoService;
        this.pedidoService = pedidoService;
        this.materiaPrimaService = materiaPrimaService;
    }


    // ===========================
    // LISTAR + FILTRO
    // ===========================
    @GetMapping("/empleado")
    public String listar(Model model, @RequestParam(required = false) String filtro) {

        List<Produccion> lista;

        if (filtro != null && !filtro.isEmpty()) {
            lista = produccionService.buscarvarioscampos(filtro);
        } else {
            lista = produccionService.listar();
        }

        model.addAttribute("producciones", lista);
        model.addAttribute("filtro", filtro);

        return "empleado/produccion-index";
    }


    // ===========================
    // FORM CREAR / EDITAR
    // ===========================
    @GetMapping("/form")
    public String form(@RequestParam(required = false) Integer id, Model model) {

        Produccion produccion = (id != null)
                ? produccionService.listar().stream()
                .filter(p -> p.getId_producc().equals(id))
                .findFirst()
                .orElse(new Produccion())
                : new Produccion();

        // Datos para selects
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        model.addAttribute("produccion", produccion);

        return "empleado/produccion-form";
    }


    // ===========================
    // GUARDAR
    // ===========================
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute Produccion produccion) {
        produccionService.guardar(produccion);
        return "redirect:/produccion/empleado";
    }


    // ===========================
    // ELIMINAR
    // ===========================
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        produccionService.eliminar(id);
        return "redirect:/produccion/empleado";
    }


    // ===========================
    // EDITAR
    // ===========================
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {

        Produccion produccion = produccionService.listar().stream()
                .filter(p -> p.getId_producc().equals(id))
                .findFirst()
                .orElse(null);

        model.addAttribute("produccion", produccion);

        // Selects FK
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "empleado/produccion-form";
    }


    // ===========================
    // BUSCAR
    // ===========================
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {

        List<Produccion> lista = produccionService.buscarvarioscampos(filtro);

        model.addAttribute("producciones", lista);
        model.addAttribute("filtro", filtro);

        return "empleado/produccion-index";
    }

}
