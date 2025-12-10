package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.DetFactCompra;
import com.sustentacion.luxyfashion.services.DetFactCompraService;
import com.sustentacion.luxyfashion.services.FacturaCompraService;
import com.sustentacion.luxyfashion.services.MateriaPrimaService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/detfactcompra")
public class DetFactCompraController {

    private final DetFactCompraService detFactCompraService;
    private final FacturaCompraService facturaCompraService;
    private final MateriaPrimaService materiaPrimaService;

    public DetFactCompraController(DetFactCompraService detFactCompraService,
                                   FacturaCompraService facturaCompraService,
                                   MateriaPrimaService materiaPrimaService) {
        this.detFactCompraService = detFactCompraService;
        this.facturaCompraService = facturaCompraService;
        this.materiaPrimaService = materiaPrimaService;
    }

    // Listar todos los detalles (con filtro opcional)
    @GetMapping()
    public String listarParaEmpleado(Model model, @RequestParam(required = false) String filtro) {
        List<DetFactCompra> lista;
        if (filtro != null && !filtro.isEmpty()) {
            lista = detFactCompraService.buscarvarioscampos(filtro);
        } else {
            lista = detFactCompraService.listar();
        }
        model.addAttribute("detFactCompra",new DetFactCompra());
        model.addAttribute("detFactCompraList", detFactCompraService.listar());
        model.addAttribute("filtro", filtro);
        return "admin/detfacturacompra/detcompra"; // Ajusta según tu plantilla
    }

    // Mostrar formulario para crear o editar
    @GetMapping("/form")
    public String mostrarFormulario(@RequestParam(required = false) Integer id, Model model) {
        DetFactCompra detFactCompra = (id != null)
                ? detFactCompraService.listar().stream()
                .filter(d -> d.getId_det_fcm().equals(id))
                .findFirst().orElse(new DetFactCompra())
                : new DetFactCompra();

        model.addAttribute("detFactCompra", detFactCompra);
        // Listas para selects
        model.addAttribute("facturas", facturaCompraService.listar());
        model.addAttribute("materias", materiaPrimaService.listar());

        return "admin/detfacturacompra/detcompra";
    }

    // Guardar o actualizar
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute DetFactCompra detFactCompra) {
        detFactCompraService.guardar(detFactCompra);
        return "redirect:/admin/detfacturacompra/editardetallecompra";
    }

    // Eliminar detalle
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        detFactCompraService.eliminar(id);
        return "redirect:/admin/detfacturacompra/detcompra";
    }

    // Buscar por filtro (puede usarse también desde la lista)
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {
        List<DetFactCompra> lista = detFactCompraService.buscarvarioscampos(filtro);
        model.addAttribute("detFactCompras", lista);
        model.addAttribute("filtro", filtro);
        return "admin/detfacturacompra/detcompra";
    }

    // Mostrar formulario de edición (alias de /form con id)
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        return mostrarFormulario(id, model);
    }
}
