package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import com.sustentacion.luxyfashion.services.DetMateriaPrimaService;
import com.sustentacion.luxyfashion.services.MateriaPrimaService;
import com.sustentacion.luxyfashion.services.ProduccionService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/detmateriaprima")
public class DetMateriaPrimaController {

    private final DetMateriaPrimaService detMateriaPrimaService;
    private final MateriaPrimaService materiaPrimaService;
    private final ProduccionService produccionService;

    public DetMateriaPrimaController(DetMateriaPrimaService detMateriaPrimaService,
                                     MateriaPrimaService materiaPrimaService,
                                     ProduccionService produccionService) {
        this.detMateriaPrimaService = detMateriaPrimaService;
        this.materiaPrimaService = materiaPrimaService;
        this.produccionService = produccionService;
    }

    // Listar todos los detalles (con filtro opcional)
    @GetMapping("/empleado")
    public String listarParaEmpleado(Model model, @RequestParam(required = false) String filtro) {
        List<DetMateriaPrima> lista;
        if (filtro != null && !filtro.isEmpty()) {
            lista = detMateriaPrimaService.buscarvarioscampos(filtro);
        } else {
            lista = detMateriaPrimaService.listar();
        }
        model.addAttribute("detMateriaPrimas", lista);
        model.addAttribute("filtro", filtro);
        return "empleado/index"; // Ajusta según tu plantilla
    }

    // Mostrar formulario para crear o editar
    @GetMapping("/form")
    public String mostrarFormulario(@RequestParam(required = false) Integer id, Model model) {
        DetMateriaPrima detMateriaPrima = (id != null)
                ? detMateriaPrimaService.listar().stream()
                .filter(d -> d.getId_det_pm().equals(id))
                .findFirst().orElse(new DetMateriaPrima())
                : new DetMateriaPrima();

        model.addAttribute("detMateriaPrima", detMateriaPrima);

        // Listas para selects
        model.addAttribute("materias", materiaPrimaService.listar());
        model.addAttribute("producciones", produccionService.listar());

        return "empleado/detmateriaprima-form";
    }

    // Guardar o actualizar
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute DetMateriaPrima detMateriaPrima) {
        detMateriaPrimaService.guardar(detMateriaPrima);
        return "redirect:/detmateriaprima/empleado";
    }

    // Eliminar detalle
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        detMateriaPrimaService.eliminar(id);
        return "redirect:/detmateriaprima/empleado";
    }

    // Buscar por filtro
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {
        List<DetMateriaPrima> lista = detMateriaPrimaService.buscarvarioscampos(filtro);
        model.addAttribute("detMateriaPrimas", lista);
        model.addAttribute("filtro", filtro);
        return "empleado/index";
    }

    // Mostrar formulario de edición (alias de /form con id)
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        return mostrarFormulario(id, model);
    }
}
