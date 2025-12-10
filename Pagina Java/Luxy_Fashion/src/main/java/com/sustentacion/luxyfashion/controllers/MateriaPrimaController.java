package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.MateriaPrima;
import com.sustentacion.luxyfashion.services.MateriaPrimaService;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/materiaprima")
public class MateriaPrimaController {

    private final MateriaPrimaService materiaPrimaService;

    public MateriaPrimaController(MateriaPrimaService materiaPrimaService) {
        this.materiaPrimaService = materiaPrimaService;
    }

    // ===========================
    // LISTAR + FILTRO
    // ===========================
    @GetMapping("/empleado")
    public String listar(Model model, @RequestParam(required = false) String filtro) {

        List<MateriaPrima> lista;

        if (filtro != null && !filtro.isEmpty()) {
            lista = materiaPrimaService.buscarvarioscampos(filtro);
        } else {
            lista = materiaPrimaService.listar();
        }

        model.addAttribute("materias", lista);
        model.addAttribute("filtro", filtro);

        return "empleado/materiaprima-index"; // Cambia según tu HTML
    }

    // ===========================
    // FORM CREAR / EDITAR
    // ===========================
    @GetMapping("/form")
    public String form(@RequestParam(required = false) Integer id, Model model) {

        MateriaPrima mp = (id != null)
                ? materiaPrimaService.listar().stream()
                .filter(m -> m.getId_matp().equals(id))
                .findFirst().orElse(new MateriaPrima())
                : new MateriaPrima();

        model.addAttribute("materiaprima", mp);

        return "empleado/materiaprima-form";
    }

    // ===========================
    // GUARDAR
    // ===========================
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute MateriaPrima materiaPrima) {
        materiaPrimaService.guardar(materiaPrima);
        return "redirect:/materiaprima/empleado";
    }

    // ===========================
    // ELIMINAR
    // ===========================
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        materiaPrimaService.eliminar(id);
        return "redirect:/materiaprima/empleado";
    }

    // ===========================
    // EDITAR
    // ===========================
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        MateriaPrima materia = materiaPrimaService.listar().stream()
                .filter(mp -> mp.getId_matp().equals(id))
                .findFirst()
                .orElse(null);

        model.addAttribute("materiaprima", materia);

        return "empleado/materiaprima-form";
    }

    // ===========================
    // BUSCAR
    // ===========================
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {

        List<MateriaPrima> lista = materiaPrimaService.buscarvarioscampos(filtro);

        model.addAttribute("materias", lista);
        model.addAttribute("filtro", filtro);

        return "empleado/materiaprima-index";
    }
}
