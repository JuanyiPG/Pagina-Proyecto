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

    // ============================================
    // LISTAR + FORMULARIO + BUSCAR
    // ============================================
    @GetMapping("")
    public String listar(Model model, @RequestParam(required = false) String filtro) {

        List<MateriaPrima> lista =
                (filtro != null && !filtro.trim().isEmpty())
                        ? materiaPrimaService.buscarvarioscampos(filtro)
                        : materiaPrimaService.listar();

        model.addAttribute("materias", lista);
        model.addAttribute("materiaprima", new MateriaPrima()); // formulario vacío
        model.addAttribute("filtro", filtro);

        return "admin/materiaprima/indexmatp";
    }

    // ============================================
    // EDITAR (CARGAR DATOS EN EL FORMULARIO)
    // ============================================
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {

        // Como NO tienes findById, se busca manualmente en la lista
        MateriaPrima materia = materiaPrimaService.listar().stream()
                .filter(mp -> mp.getId_matp().equals(id))
                .findFirst()
                .orElse(new MateriaPrima());

        model.addAttribute("materiaprima", materia);
        model.addAttribute("materias", materiaPrimaService.listar());

        return "admin/materiaprima/indexmatp";
    }

    // ============================================
    // GUARDAR
    // ============================================
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute MateriaPrima materiaPrima) {
        materiaPrimaService.guardar(materiaPrima);
        return "redirect:/admin/materiaprima";
    }

    // ============================================
    // ELIMINAR
    // ============================================
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        materiaPrimaService.eliminar(id);
        return "redirect:/admin/materiaprima";
    }

    // ============================================
    // BUSCAR
    // ============================================
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {

        List<MateriaPrima> lista = materiaPrimaService.buscarvarioscampos(filtro);

        model.addAttribute("materias", lista);
        model.addAttribute("materiaprima", new MateriaPrima());
        model.addAttribute("filtro", filtro);

        return "admin/materiaprima/indexmatp";
    }
}
